from dataclasses import fields
# from django import forms
from django.forms import TextInput, EmailInput, PasswordInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
# from django import forms


class Register(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']
        widgets = {
            'first_name': TextInput(attrs={
                'class': "form-control",
                }),
            'last_name': TextInput(attrs={
                'class': "form-control",
                }),
            'username': TextInput(attrs={
                'class': "form-control",
                }),
            'email': EmailInput(attrs={
                'class': "form-control", 
                }),
            'password1': PasswordInput(attrs={
                'class': "form-control",
                }),
            'password2': PasswordInput(attrs={
                'class': "form-control",
                }),
        }
