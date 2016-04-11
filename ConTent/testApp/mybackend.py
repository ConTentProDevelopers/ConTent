from django.conf import settings
from testApp.models import MyUser


class SettingsBackend(object):
    """
    Authenticate against the settings ADMIN_LOGIN and ADMIN_PASSWORD.

    Use the login name, and a hash of the password. For example:

    ADMIN_LOGIN = 'admin'
    ADMIN_PASSWORD = 'pbkdf2_sha256$30000$Vo0VlMnkR4Bk$qEvtdyZRWTcOsCnI/oQ7fVOu1XAURIZYoOZ3iq8Dr4M='
    """

    def authenticate(self, username=None, password=None):
        login_valid = (settings.ADMIN_LOGIN == username)
        print(login_valid)
        print(settings.ADMIN_LOGIN)
        pwd_valid = (password == settings.ADMIN_PASSWORD)
        print(pwd_valid)
        print(settings.ADMIN_PASSWORD)
        print(password)
        if login_valid and pwd_valid:
            try:
                user = MyUser.objects.get(email=username)
            except MyUser.DoesNotExist:
                # Create a new user. Note that we can set password
                # to anything, because it won't be checked; the password
                # from settings.py will.
                user = MyUser(email=username, password='get from settings.py')
                user.is_superuser = True
                user.save()
            return user
        return None

    def get_user(self, user_id):
        try:
            return MyUser.objects.get(pk=user_id)
        except MyUser.DoesNotExist:
            return None