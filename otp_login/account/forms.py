from django import forms

class OTPForm(forms.Form):
    """
    OTP form to authenticate the user
    """

    username = forms.CharField()

    otp = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'OTP'}),
    )


    def clean(self):
        if not self.cleaned_data.get('otp'):
            raise forms.ValidationError({
                'otp': 'Invalid OTP'
            })

        return self.cleaned_data
