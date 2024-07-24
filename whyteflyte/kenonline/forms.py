from django.contrib.auth.forms import UserCreationForm as ucf, AuthenticationForm as af
from django.contrib.auth.models import User
from django import forms
from django.forms.widgets import PasswordInput, TextInput
class CreateUserForm(ucf):

    class Meta:

        model = User
        fields = ['username', 'email', 'password1', 'password2']


class LoginForm(af):

    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())

