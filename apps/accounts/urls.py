from django.urls import path
from . import views
from .views import profile_redirect_view, complete_profile_view

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.choose_register_view, name="register"),  
    path("register/cliente/", views.register_cliente_view, name="register_cliente"),
    path("register/oficina/", views.register_oficina_view, name="register_oficina"),
    path("profile-redirect/", profile_redirect_view, name="profile_redirect"),
    path("complete-profile/", complete_profile_view, name="complete_profile"),
]
