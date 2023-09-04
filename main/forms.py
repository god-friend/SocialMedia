from typing import Any
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import Users
from django import forms

class ChangeUserForm(forms.ModelForm):
    __form_attrs = {"class": "form-control"}
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "disabled": True}))
    firstname = forms.CharField(widget=forms.TextInput(attrs=__form_attrs))
    lastname = forms.CharField(widget=forms.TextInput(attrs=__form_attrs))
    profile_pic = forms.FileField(widget=forms.FileInput(attrs=__form_attrs), required=False)

    class Meta:
        model = Users
        fields = ["username", "firstname", "lastname", "profile_pic"]



class CreateUserForm(UserCreationForm):
    __form_attrs = {"class": "form-control"}
    username = forms.CharField(max_length=256, widget=forms.TextInput(attrs=__form_attrs),
                               min_length=3, error_messages={"too_short": "Username must contain atlest 3 aphabets"})
    firstname = forms.CharField(max_length=256, widget=forms.TextInput(attrs=__form_attrs))
    lastname = forms.CharField(max_length=256, widget=forms.TextInput(attrs=__form_attrs))
    password1 = forms.CharField(max_length=256, widget=forms.PasswordInput(attrs=__form_attrs), 
                                label="Password")
    password2 = forms.CharField(max_length=256, widget=forms.PasswordInput(attrs=__form_attrs),
                                label="Confirm Password")

    class Meta:
        model = Users
        fields = ["username", "firstname", "lastname", "password1", "password2"]


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=256)
    username.widget = forms.TextInput(attrs={"class": "form-control"})
    password = forms.CharField(max_length=256)
    password.widget = forms.PasswordInput(attrs={"class": "form-control"})
    error_messages = {
        "invalid_login": "Username Password Doesn't match"
    }
    class Meta:
        model = Users
        fields = "__all__"
        

