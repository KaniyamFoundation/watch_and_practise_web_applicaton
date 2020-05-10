from django.shortcuts import render, redirect, HttpResponse
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from datetime import datetime, date
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.db.models import Q
from django.utils import timezone

from streamapp.utils import account_activation_token, get_shell_url_for_user
from streamapp.models import Event, StreamEvent


# Create your views here.

class SignupPageView(View):
    """
        endpoint: /signup
        purpose: "handles signup of an user"
    """
    def get(self, request):
        """

        :param request: None
        :return: render signup form with fields email, first_name, last_name, passowrd
        """
        template_name = 'signup.html'
        context = {"signup_page": "active"}
        return render(request, template_name=template_name, context=context)

    def post(self, request):
        """
        :param request: email and password, confirm_password are mandatory to this api
        :return: sends success message if signup success, else display error messages
        """
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        c_password = request.POST.get('password_confirmation')
        if c_password != password:
            context = {"signup_page": "active", "messages": {"level": "danger", "short": "Error!",
                                                             "msg": "Password doesn't match with confirm password"}}
            return render(request, template_name='signup.html', context=context)

        user = User.objects.filter(username=email)

        if user.exists():
            context = {"signup_page": "active", "messages": {"level": "danger", "short": "Error!",
                                                             "msg": "Email address already exists"}}
            return render(request, template_name='signup.html', context=context)
        elif email and password:
            u = User()
            u.username = email
            u.email = email
            u.first_name = first_name
            u.last_name = last_name
            u.set_password(password)
            u.is_active = False
            u.save()

            #email part
            mail_subject = 'Activate your user account.'
            current_site = get_current_site(request)
            message = render_to_string('acc_active_email.html', {
                'user': u,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(u.pk)),
                'token': account_activation_token.make_token(u),
            })
            to_email = email
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            context = {"signup_page": "active", "messages": {"level": "success", "short": "Success! ",
                                                             "msg": "Please confirm your email address to "
                                                                    "complete the registration"}}
            return render(request, template_name='signup.html', context=context)

        return


class ActivateView(View):
    """
        This is an view for activating email link for view
    """
    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            current_site = get_current_site(request)
            url = "http://" + current_site.domain + "/login/"
            msg = 'Thank you for your email confirmation. Now you can login your account <a href=%s >here</a>' % url
            return HttpResponse(msg)
        else:
            return HttpResponse('Activation link is invalid!')


class LoginPageView(View):
    """
        endpoint: /login
        purpose: to authenticate users
    """

    def get(self, request):
        """
        :param request: None
        :return: render login form with username and password fields
        """
        template_name = 'login.html'
        context = {"login_page": "active"}
        return render(request, template_name=template_name, context=context)

    def post(self, request):
        """
        :param request: email, password are needed to authenticate
        :return: if login success redirect to another page else display error message
        """

        template_name = 'login.html'
        context = {"login_page": "active"}
        username = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.filter(username=username).first()
        if user is not None and not user.is_active:
            context["messages"] = {"msg": "Email Verification Pending", "level": "danger", "short": "Error! "}
            return render(request=request, template_name=template_name, context=context)

        if user is not None:
            # A backend authenticated the credentials
            user = authenticate(username=username, password=password)
            if user and user.is_authenticated:
                login(request, user)
                context["messages"] = {"msg": "login successful", "level": "success", "short": "Success! "}
                return redirect(self.request.GET.get('next', '/'))

            else:
                context["messages"] = {"msg": "wrong password", "level": "danger", "short": "Error! "}
                return render(request=request, template_name=template_name, context=context)
        else:
            # No backend authenticated the credentials
            context["messages"] = {"msg": "User not found", "level": "danger", "short": "Error! "}
            return render(request=request, template_name=template_name, context=context)


class LogoutView(View):
    """
        endpoint: /logout
        purpose: Handles logout of an user
    """
    def get(self, request):
        """
        :param request: request headers
        :return: renders login page
        """
        logout(request)
        return redirect('/login')


class AboutPageView(View):
    """
        endpoint: /about
        purpose: this handles about page views
    """

    def get(self, request):
        """
        :param request: None
        :return: render about page
        """
        template_name = 'about.html'
        context = {"about_page": "active"}
        return render(request=request, template_name=template_name, context=context)


class HomeView(View):
    """
    This view handles home page requests
    """
    
    def get(self, request):
        """

        :param request: None
        :return: render signup form with fields email, first_name, last_name, passowrd
        """
        template_name = 'home.html'
        context = {"home_page": "active"}
        queryset = Q(is_active=True, is_deleted=False)
        order_by_field = '-event_date'
        
        # get search query here
        search_q = request.GET.get('q')
        filter_q = request.GET.get('filter_by')
        
        # include search condition also here
        if search_q:
            queryset &= Q(title__icontains=search_q) | Q(tags__name__icontains=search_q)| Q(category__name__icontains=search_q)
        
        if filter_q and filter_q in ["Today", "Upcoming", "Past"]:
            if filter_q == 'Past':
                queryset &= Q(event_date__lte=datetime.now())
            elif filter_q == 'Upcoming':
                queryset &= Q(event_date__gte=datetime.now())
            else:
                queryset &= Q(event_date__startswith=date.today())
        print("*****", queryset)
        events_obj = Event.objects.filter(queryset).order_by(order_by_field).distinct()
        
        # block view if it's future
        for event in events_obj:
            if event.event_date > timezone.now():
                event.can_view = False
                event.flag = "upcoming"
                event.event_url = "#"
            else:
                event.can_view = True
                event.flag = "current"
                event.event_url = "/event/{}".format(str(event.event_id))
            print("event_date", event.event_date)
            print("timezone date", timezone.now())
        context = {"events": events_obj, "filter": filter_q, "q": search_q}
        return render(request, template_name=template_name, context=context)
    
    @login_required
    def post(self, request):
        pass


class StreamViewAPI(View):
    """
        This view handles streaming of an event (live, past) both type
    """
    def get(self, request, event_id):
        template_name = 'index.html'
        context = {}
        
        # if not logged in redirect to login
        if not request.user.is_authenticated:
            return redirect('/login')

        event = Event.objects.get(event_id=event_id)
        stream_obj = StreamEvent.objects.get(event=event)
        
        # get etherpad and youtube url from model
        context["youtube_url"] = stream_obj.youtube_url
        context["etherpad_url"] = stream_obj.youtube_url
        
        # find the folder path and ttyd url for this user
        context["shell_url"] = get_shell_url_for_user(request.user)
        
        return render(request, template_name=template_name, context=context)