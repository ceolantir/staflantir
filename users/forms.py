from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'password1',
            'password2',
            'email',
        ]


class ProfileForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'email': 'Почта',
        }


class ChangePasswordForm(forms.Form):
    password_now = forms.CharField(widget=forms.PasswordInput(), label='Текущий пароль')
    password_new = forms.CharField(widget=forms.PasswordInput(), label='Новый пароль')

    class Meta:
        fields = ('password_now', 'password_new')
