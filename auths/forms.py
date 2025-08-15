from dataclasses import fields

# from django import forms
from django.forms import TextInput, EmailInput, PasswordInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# from django import forms


class Register(UserCreationForm):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2",
        ]
        widgets = {
            "first_name": TextInput(
                attrs={
                    "class": "w-full px-4 py-2 border border-green-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-400 bg-white text-green-900",
                }
            ),
            "last_name": TextInput(
                attrs={
                    "class": "w-full px-4 py-2 border border-green-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-400 bg-white text-green-900",
                }
            ),
            "username": TextInput(
                attrs={
                    "class": "w-full px-4 py-2 border border-green-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-400 bg-white text-green-900",
                }
            ),
            "email": EmailInput(
                attrs={
                    "class": "w-full px-4 py-2 border border-green-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-400 bg-white text-green-900",
                }
            ),
            "password1": PasswordInput(
                attrs={
                    "class": "w-full px-4 py-2 border border-green-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-400 bg-white text-green-900",
                }
            ),
            "password2": PasswordInput(
                attrs={
                    "class": "w-full px-4 py-2 border border-green-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-400 bg-white text-green-900",
                }
            ),
        }
