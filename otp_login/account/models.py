from django.db import models
from django.utils import timezone
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

    otp_last_generated = models.DateTimeField(auto_now=True)


    @property
    def generate_otp(self):
        return User.objects.make_random_password(length=6, allowed_chars='0123456789')

    @property
    def get_otp(self):
        if (not self.otp or
            timezone.now() > self.otp_last_generated + timezone.timedelta(minutes=settings.OTP_VALIDITY)):
            self.otp = self.generate_otp()
            self.save()
        return self.otp

    @property
    def validate_otp(self, otp):
        if (self.otp and
            timezone.now < self.otp_last_generated + timezone.timedelta(minutes=settings.OTP_VALIDITY)):
            self.otp = None
            self.save()
            return True
        return False
