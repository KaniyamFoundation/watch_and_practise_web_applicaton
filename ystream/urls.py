"""ystream URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path

from streamapp.views import HomeView, SignupPageView, LoginPageView, AboutPageView, LogoutView, ActivateView, \
    StreamViewAPI
from django.contrib.auth import views as auth_views
from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('signup/', SignupPageView.as_view(), name='signup'),
    path('login/', LoginPageView.as_view(), name='login'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
    re_path(r'^password_reset/$',
            auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'),
            name='password_reset'),
    re_path(r'^password_reset/done/$', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    re_path(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    re_path(r'^reset/done/$', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        ActivateView.as_view(), name='activate'),
    
    path('event/<uuid:event_id>', StreamViewAPI.as_view(), name='stream'),
]
