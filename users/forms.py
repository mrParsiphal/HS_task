from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import UserProfile
from django import forms


class LoginForm(forms.Form):
    phone_number = forms.CharField(
        label='Номер телефона',
        max_length=18,
    )

    class Meta:
        model = UserProfile
        fields = 'phone_number'


class CabinetForm(forms.Form):
    subscription = forms.CharField(
        label='Введите код другого пользователя для подписки',
        max_length=6,
    )

    class Meta:
        model = UserProfile
        fields = 'subscription'
