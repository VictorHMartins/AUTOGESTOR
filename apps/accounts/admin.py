from django.contrib import admin
from .models import User, ClienteProfile, OficinaProfile


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "user_type", "get_phone", "get_cpf")
    search_fields = ("username", "email")
    list_filter = ("user_type",)

    def get_phone(self, obj):
        if obj.user_type == "cliente" and hasattr(obj, "cliente_profile"):
            return obj.cliente_profile.phone
        elif obj.user_type == "oficina" and hasattr(obj, "oficina_profile"):
            return obj.oficina_profile.phone
        return "-"
    get_phone.short_description = "Telefone"

    def get_cpf(self, obj):
        if obj.user_type == "cliente" and hasattr(obj, "cliente_profile"):
            return obj.cliente_profile.cpf
        elif obj.user_type == "oficina" and hasattr(obj, "oficina_profile"):
            return obj.oficina_profile.cnpj
        return "-"
    get_cpf.short_description = "CPF/CNPJ"


@admin.register(ClienteProfile)
class ClienteProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "phone", "cpf", "data_nascimento", "city", "state")
    search_fields = ("user__username", "user__email", "cpf")


@admin.register(OficinaProfile)
class OficinaProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "nome_fantasia", "cnpj", "phone", "city", "state")
    search_fields = ("user__username", "user__email", "cnpj")
