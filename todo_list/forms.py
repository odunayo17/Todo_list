from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Todo
from django import forms
import re


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = "__all__"
        exclude = ["user"]

        widgets = {
            "add": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Add Todo List",
                }
            ),
        }


"""
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
        ]

    def clean_email(self):
        email = self.cleaned_data["email"]
        # Add custom validation logic for the email field, if needed.
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email"""

"""
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = (
            "username",
            "email",
            "password1",
            "password2",
            "first_name",
            "last_name",
        )

    def clean_email(self):
        email = self.cleaned_data["email"]
        User = get_user_model()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        if (
            len(password1) < 9
            or not any(char.isalpha() for char in password1)
            or not any(char.isdigit() for char in password1)
        ):
            raise forms.ValidationError(
                "Password must be at least 9 characters long and contain both letters and numbers."
            )
        return password1

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
"""


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        max_length=254,
        required=True,
        widget=forms.EmailInput(attrs={"class": "form-control"}),
        error_messages={
            "required": "Email is required.",
            "invalid": "Please enter a valid email address.",
            "unique": "This email is already registered.",
        },
    )

    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")

        if password1 and not password1.isalnum():
            raise forms.ValidationError("Password must be alphanumeric.")

        return password2

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name")
