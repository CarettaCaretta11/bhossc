from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Room, User


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = ['thumbnail', 'name', 'description']


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'password1', 'password2']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'name', 'username', 'email', 'bio']
