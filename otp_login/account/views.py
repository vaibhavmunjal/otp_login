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
