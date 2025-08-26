from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import RegisterForm, ClienteProfileForm, OficinaProfileForm
from .models import User


# 🔹 Tela inicial para escolher tipo de cadastro
def choose_register_view(request):
    return render(request, "accounts/auth/choose_register.html")


# 🔹 Cadastro de Cliente
def register_cliente_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = "cliente"
            user.set_password(form.cleaned_data["password1"])  # password1 do UserCreationForm
            user.save()
            messages.success(request, "Conta de cliente criada com sucesso! Faça login.")
            return redirect("login")
    else:
        form = RegisterForm()
    return render(request, "accounts/auth/register.html", {"form": form, "tipo": "Cliente"})


# 🔹 Cadastro de Oficina
def register_oficina_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = "oficina"
            user.set_password(form.cleaned_data["password1"])
            user.save()
            messages.success(request, "Conta de oficina criada com sucesso! Faça login.")
            return redirect("login")
    else:
        form = RegisterForm()
    return render(request, "accounts/auth/register.html", {"form": form, "tipo": "Oficina"})


# 🔹 Login
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("profile_redirect")  # leva para o redirecionamento de perfil
    else:
        form = AuthenticationForm()
    return render(request, "accounts/auth/login.html", {"form": form})


# 🔹 Logout
def logout_view(request):
    logout(request)
    return redirect("login")


# 🔹 Redirecionamento pós-login
@login_required
def profile_redirect_view(request):
    user = request.user

    if user.user_type == "cliente":
        if not hasattr(user, "cliente_profile") or not user.cliente_profile.cpf or not user.cliente_profile.phone:
            return redirect("complete_profile")

    elif user.user_type == "oficina":
        if not hasattr(user, "oficina_profile") or not user.oficina_profile.cnpj or not user.oficina_profile.phone:
            return redirect("complete_profile")

    return redirect("home")


# 🔹 Completar Perfil (Cliente ou Oficina)
@login_required
def complete_profile_view(request):
    user = request.user

    if user.user_type == "cliente":
        profile = user.cliente_profile
        form_class = ClienteProfileForm
    else:
        profile = user.oficina_profile
        form_class = OficinaProfileForm

    if request.method == "POST":
        form = form_class(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil atualizado com sucesso!")
            return redirect("home")
        else:
            messages.error(request, "Corrija os erros do formulário.")
    else:
        form = form_class(instance=profile)

    return render(request, "accounts/auth/complete_profile.html", {"form": form, "tipo": user.get_user_type_display()})
