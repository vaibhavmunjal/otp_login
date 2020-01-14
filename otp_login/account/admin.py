from django.contrib import admin

# Register your models here.

from .models import OTPUser

admin.site.register(OTPUser)