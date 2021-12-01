from django import forms
from django.forms.widgets import DateInput
from django.contrib.auth.forms import (
    AuthenticationForm, UsernameField, UserCreationForm)
from django.contrib.auth.models import User

from .models import Profile


class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'placeholder': 'например: Fedor',
                                                           'class': 'form-control', }))

    password = forms.CharField(
        label="Пароль",
        strip=False,
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Пароль', 'class': 'form-control'}),
    )

    error_messages = {
        'invalid_login': "Введен неправильный логин или пароль",
    }


class SignUpForm(UserCreationForm):
    password1 = forms.CharField(
        label='Пароль',
        strip=False,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Пароль',
            'class': 'form-control',
        }),
    )

    password2 = forms.CharField(
        label='Подтвердите пароль',
        strip=False,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Повторите пароль',
            'class': 'form-control',
        }),
        # help_text='Введите тот же пароль, что и выше'
    )

    error_messages = {
        'password_mismatch': 'Пароли не совпадают'
    }

    class Meta:
        model = User
        fields = ['email', 'username']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Логин'}),
            'email': forms.EmailInput(attrs={'autofocus': True, 'class': 'form-control', 'placeholder': 'Ваш email'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError('email должен быть уникальным')
        return email


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['about', 'foto', 'birth_date']
        labels = {
            'about': 'Обо мне',
            'foto': 'Мое фото',
            'birth_date': 'Мой день рождения',
        },
        widgets = {
            'birth_date': DateInput(attrs={'type': 'date', 'placeholder': 'дата рождения'})
        }
