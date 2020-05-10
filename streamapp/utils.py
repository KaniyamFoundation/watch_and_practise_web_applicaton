from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six
import os
import hashlib



def task_finished(filedata):
    try:
        subject = "Your file has been converted into mp3 Successfully %s" % filedata["file_name"]
        To = filedata.get('user').get('email')
        d_link = settings.SERVER_URL + filedata.get("output_file")
        text = """
                Hi $FIRST_NAME,
                    Your file has been successfully converted to mp3. Please login to your account and
                    download the file from your home page or click the below link to download now.
                    $D_LINK
        """.replace('$FIRST_NAME', filedata.get('user', {}).get('first_name', '')).replace('$D_LINK', d_link)
        send_mail(
            subject,
            text,
            settings.FROM_EMAIL,
            [To],
            fail_silently=False)
        return True
    except Exception as e:
        print(str(e))
        return False


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.is_active)
        )


account_activation_token = TokenGenerator()


def get_shell_url_for_user(user):
    shell_url = os.environ.get('SERVER_URL') + "/ttyd/"
    guests_base_dir = os.environ.get('GUEST_BASE_DIR')
    
    # hash user email by sha256
    result = hashlib.sha256(user.email.encode())
    
    # specified user directory path
    create_dir_path = guests_base_dir + result.hexdigest()
    
    # if path already exists ignore
    #os.makedirs(create_dir_path, exist_ok=True)
    
    # for shell url now with user directory path
    shell_url += "?arg={}&arg={}".format(create_dir_path, str(user.id))
    return shell_url
