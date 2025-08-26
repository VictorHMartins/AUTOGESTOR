from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import RegisterForm, ClienteProfileForm, OficinaProfileForm
from .models import User, ClienteProfile, OficinaProfile


# 🔹 Tela inicial para escolher tipo de cadastro
def choose_register_view(request):
    return render(request, "accounts/auth/choose_register.html")


# 🔹 Cadastro de Cliente (fluxo normal)
def register_cliente_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = "cliente"
            user.save()

            # Atualizar perfil criado pelo signal
            profile = user.cliente_profile
            profile.phone = form.cleaned_data["phone"]
            profile.cpf = form.cleaned_data["cpf"]
            profile.save()

            # Autenticar e logar com backend definido
            raw_password = form.cleaned_data["password1"]
            user = authenticate(request, email=user.email, password=raw_password)
            login(request, user, backend="django.contrib.auth.backends.ModelBackend")

            messages.success(request, "Conta criada com sucesso!")
            return redirect("home")
        else:
            messages.error(request, "Corrija os erros do formulário.")
    else:
        form = RegisterForm()
    return render(request, "accounts/auth/register.html", {"form": form, "tipo": "Cliente"})


def register_oficina_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = "oficina"
            user.save()

            # Atualizar perfil criado pelo signal
            profile = user.oficina_profile
            profile.nome_fantasia = user.first_name
            profile.save()

            # Autenticar e logar corretamente
            raw_password = form.cleaned_data["password1"]
            user = authenticate(request, email=user.email, password=raw_password)
            login(request, user, backend="django.contrib.auth.backends.ModelBackend")

            messages.success(request, "Conta de oficina criada com sucesso!")
            return redirect("home")
        else:
            messages.error(request, "Corrija os erros do formulário.")
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
            return redirect("profile_redirect")
        else:
            messages.error(request, "Usuário ou senha inválidos.")
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
        profile = getattr(user, "cliente_profile", None)
        if not profile or not profile.cpf or not profile.phone or not profile.data_nascimento or not profile.city:
            return redirect("complete_profile")

    elif user.user_type == "oficina":
        profile = getattr(user, "oficina_profile", None)
        if not profile or not profile.cnpj or not profile.phone or not profile.city:
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
