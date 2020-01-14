from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend


User = get_user_model()


class OTPModelBackEnd(BaseBackend):
    """
    OTP Based Login For Users
    """

    def authenticate(self, request, username, otp):
        try:
            user = User.objects.select_related('otp').get(username=username)
        except User.DoesNotExist:
            return None
        else:
            if (hasattr(user, 'otp') and
                user.otp.validate_otp(otp=otp)):
                return user

        return None



    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

