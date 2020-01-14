from django.db import models
from django.utils import timezone
from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
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


    def __str__(self):
        return self.user.username


    def generate_otp(self):
        return User.objects.make_random_password(length=6, allowed_chars='0123456789')

    def get_otp(self):
        if (not self.otp or
            timezone.now() > self.otp_last_generated + timezone.timedelta(minutes=settings.OTP_VALIDITY)):
            self.otp = self.generate_otp()
            self.save()
        return self.otp

    def validate_otp(self, otp):
        if (otp == self.otp and
            timezone.now() < self.otp_last_generated + timezone.timedelta(minutes=settings.OTP_VALIDITY)):
            self.otp = None
            self.save()
            return True
        return False


@receiver(post_save, sender=User)
def _post_otp_save(sender, instance, created, **kwargs):
    if created:
        OTPUser.objects.create(user=instance)
