from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import RegisterForm


# 🔹 Tela inicial para escolher tipo de cadastro
def choose_register_view(request):
    return render(request, "accounts/choose_register.html")


# 🔹 Cadastro de Cliente
def register_cliente_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = "cliente"   # fixa como cliente
            user.set_password(form.cleaned_data["password"])
            user.save()
            messages.success(request, "Conta de cliente criada com sucesso! Faça login.")
            return redirect("login")
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form, "tipo": "Cliente"})


# 🔹 Cadastro de Oficina
def register_oficina_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = "oficina"   # fixa como oficina
            user.set_password(form.cleaned_data["password"])
            user.save()
            messages.success(request, "Conta de oficina criada com sucesso! Faça login.")
            return redirect("login")
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form, "tipo": "Oficina"})


# 🔹 Login
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("/")  # depois mandamos para dashboard
    else:
        form = AuthenticationForm()
    return render(request, "accounts/login.html", {"form": form})


# 🔹 Logout
def logout_view(request):
    logout(request)
    return redirect("login")
