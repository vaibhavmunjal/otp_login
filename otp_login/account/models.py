from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class OTPUser(models.Model):
    """
    otp model to authenticate
    """

    user = models.OneToOneField(User,
                            verbose_name=_("User"),
                            on_delete=models.CASCADE,
                            related_name='otp')

    otp = models.CharField(_("OTP"),
                        max_length=6,
                        blank=True,
                        null=True)

    @property
    def generate_otp(self):
        return User.objects.make_random_password(length=6, allowed_chars='0123456789')
