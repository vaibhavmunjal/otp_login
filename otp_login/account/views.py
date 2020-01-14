from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.utils.encoding import force_text
from django.views.generic import FormView, TemplateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import RedirectView
from .models import OTPUser
from .forms import OTPForm


from django.contrib.auth import get_user_model

class OTPView(FormView):
    """
    OTP Login Form View
    """
    form_class = OTPForm
    template_name = 'account/login.html'
    success_url = reverse_lazy('account:success')


    def get(self, request, *args, **kwargs):
        """
        If user already logged In
        """
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.success_url)

        return super(self.__class__, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        """
        authenticate user otp
        """

        username = form.cleaned_data.get('username')
        otp = form.cleaned_data.get('otp')


        user = authenticate(username=username, otp=otp)
        # user = authenticate(username=username, password=otp)

        if user and user.is_active:
            login(self.request, user)
            return super(self.__class__, self).form_valid(form)

        # messages.error(self.request, 'Invalid OTP')
        return self.render_to_response(self.get_context_data(form=form))


class SuccessView(TemplateView):
    """
    Home/ Success page
    """
    template_name = 'account/success.html'


class Logout(RedirectView):

    pattern_name = 'account:otplogin'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(self.__class__, self).get(request, *args, **kwargs)



# DRF VIEW For API Call
# These import should be on top
# Just to separately identify them they are here

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

class GetUserAPI(APIView):

    def post(self, request, *args, **kwargs):
        otp = None
        username = request.POST.get('username')
        user = get_user_model().objects.filter(username=username).first()
        if user:
            otp = user.otp.get_otp()
            print('================')
            print(otp)
            print('================')
            return Response({"otp": otp},status=status.HTTP_200_OK)
        return Response({"otp": 'No user found'},status=status.HTTP_400_BAD_REQUEST)
