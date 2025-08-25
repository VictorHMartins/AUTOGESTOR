from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.choose_register_view, name="register"),  # tela de escolha
    path("register/cliente/", views.register_cliente_view, name="register_cliente"),
    path("register/oficina/", views.register_oficina_view, name="register_oficina"),
]
