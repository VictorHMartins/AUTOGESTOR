from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, ClienteProfile, OficinaProfile


class RegisterForm(UserCreationForm):
    user_type = forms.ChoiceField(choices=User.USER_TYPE_CHOICES, label="Tipo de usuário")

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "user_type"]


class ClienteProfileForm(forms.ModelForm):
    class Meta:
        model = ClienteProfile
        fields = ["phone", "cpf", "data_nascimento", "city", "state"]


class OficinaProfileForm(forms.ModelForm):
    class Meta:
        model = OficinaProfile
        fields = ["nome_fantasia", "cnpj", "phone", "city", "state"]
