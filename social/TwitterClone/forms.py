from typing import Any
from django import forms
from .models import Meeps, Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class ProfilePicForm(forms.ModelForm):
    profileImage = forms.ImageField(label="Profile picture")
    profileBio = forms.CharField(required=False, label="Profile Bio", \
                                  widget=forms.Textarea(attrs={"class": \
                                    "form-control", "placeholder": "profile bio"}))
    
    class Meta:
        model = Profile
        fields = ("profileImage", "profileBio", )


class MeepFrom(forms.ModelForm):
    body = forms.CharField(required=True, label="",
                           widget=forms.widgets.Textarea(
                                attrs={
                                    "placeholder": "Enter your Meep",
                                    "class": "form-control",
                                      }
                            ))
    
    class Meta: 
        model = Meeps
        exclude = ("user","likes", )


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Email address"})) 
    first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "First name"})) 
    last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Last name"}))

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'