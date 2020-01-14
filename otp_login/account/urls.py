from django.urls import path


from .views import OTPView, SuccessView, Logout, GetUserAPI


app_name = 'account'

urlpatterns = [
    path('success', SuccessView.as_view(), name='success'),
    path('', OTPView.as_view(), name='otplogin'),
    path('logout', Logout.as_view(), name='logout'),

    # API
    path('getuser', GetUserAPI.as_view(), name='getuser')
]
