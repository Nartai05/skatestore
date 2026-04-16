from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegistrationForm(UserCreationForm):
    # Используем forms.EmailField, а не models
    email = forms.EmailField(required=True, help_text='Введите действующий email')

    class Meta:
        model = User
        fields = ("username", "email")