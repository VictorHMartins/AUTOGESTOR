from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
import re
from .models import User, ClienteProfile, OficinaProfile


# 🔹 Validadores extras
def validar_cpf(value):
    if not re.match(r"^\d{11}$", value):
        raise ValidationError("Digite um CPF válido com 11 números.")


def validar_telefone(value):
    if not re.match(r"^\(?\d{2}\)?\s?9?\d{4}-?\d{4}$", value):
        raise ValidationError("Digite um telefone válido. Ex: (11) 91234-5678")


def validar_senha_forte(value):
    if (not re.search(r"[A-Z]", value) or
        not re.search(r"[a-z]", value) or
        not re.search(r"[0-9]", value) or
        not re.search(r"[@$!%*?&]", value)):
        raise ValidationError("A senha deve conter maiúscula, minúscula, número e símbolo.")


# 🔹 Formulário de Registro (Cadastro Normal)
class RegisterForm(UserCreationForm):
    first_name = forms.CharField(label="Nome completo")
    phone = forms.CharField(label="Telefone", validators=[validar_telefone])
    cpf = forms.CharField(label="CPF", validators=[validar_cpf])
    email = forms.EmailField(label="E-mail")

    class Meta:
        model = User
        fields = ["first_name", "email", "phone", "cpf", "password1", "password2"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError("Este e-mail já está cadastrado.")
        return email

    def clean_cpf(self):
        cpf = self.cleaned_data.get("cpf")
        if ClienteProfile.objects.filter(cpf=cpf).exists():
            raise ValidationError("Este CPF já está cadastrado.")
        return cpf

    def clean_password1(self):
        password = self.cleaned_data.get("password1")
        validar_senha_forte(password)
        return password


# 🔹 Completar Perfil (Cliente)
class ClienteProfileForm(forms.ModelForm):
    phone = forms.CharField(validators=[validar_telefone])
    cpf = forms.CharField(validators=[validar_cpf])

    class Meta:
        model = ClienteProfile
        fields = ["phone", "cpf", "data_nascimento", "city", "state"]

    def clean_cpf(self):
        cpf = self.cleaned_data.get("cpf")
        qs = ClienteProfile.objects.filter(cpf=cpf)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError("Este CPF já está cadastrado.")
        return cpf


# 🔹 Completar Perfil (Oficina)
class OficinaProfileForm(forms.ModelForm):
    class Meta:
        model = OficinaProfile
        fields = ["nome_fantasia", "cnpj", "phone", "city", "state"]
