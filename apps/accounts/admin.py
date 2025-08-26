from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, ClienteProfile, OficinaProfile


class UserAdmin(BaseUserAdmin):
    # usar email no lugar de username
    ordering = ("email",)
    list_display = ("email", "first_name", "last_name", "is_staff", "is_active", "user_type")
    search_fields = ("email", "first_name", "last_name")

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Informações pessoais", {"fields": ("first_name", "last_name", "user_type")}),
        ("Permissões", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Datas importantes", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "is_staff", "is_active", "user_type"),
        }),
    )


# registrar User com UserAdmin customizado
admin.site.register(User, UserAdmin)


# registrar ClienteProfile
@admin.register(ClienteProfile)
class ClienteProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "phone", "cpf", "data_nascimento", "city", "state")
    search_fields = ("user__email", "cpf")   # username removido


# registrar OficinaProfile
@admin.register(OficinaProfile)
class OficinaProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "nome_fantasia", "cnpj", "phone", "city", "state")
    search_fields = ("user__email", "cnpj")  # username removido
