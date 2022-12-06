from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()


class SignUpForm(UserCreationForm):


    username = forms.CharField(
        max_length=50,
        required=True,
        label="",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Phone Number.  ie 071001000",
            }
        ),
    )
    
    email = forms.EmailField(
        max_length=254,
        required=True,
        label="",
        #  help_text='Required.Enter valid email.Required wen if you forot password.',
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Email..."}
        ),
    )

   
    password1 = forms.CharField(
        required=True,
        label="",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Password..."}
        ),
    )

    password2 = forms.CharField(
        required=True,
        label="",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Confirm password..."}
        ),
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


