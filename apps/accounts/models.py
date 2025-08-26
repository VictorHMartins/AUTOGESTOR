from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('cliente', 'Cliente'),
        ('oficina', 'Oficina'),
    )

    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPE_CHOICES,
        default='cliente'
    )

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"


class ClienteProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cliente_profile")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefone")
    cpf = models.CharField(max_length=20, blank=True, null=True, unique=True, verbose_name="CPF")
    data_nascimento = models.DateField(null=True, blank=True, verbose_name="Data de Nascimento")
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name="Cidade")
    state = models.CharField(max_length=50, blank=True, null=True, verbose_name="Estado")

    def __str__(self):
        return f"Cliente: {self.user.username}"

    class Meta:
        verbose_name = "Perfil de Cliente"
        verbose_name_plural = "Perfis de Clientes"


class OficinaProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="oficina_profile")
    nome_fantasia = models.CharField(max_length=150, verbose_name="Nome Fantasia")
    cnpj = models.CharField(max_length=20, unique=True, null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefone")
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name="Cidade")
    state = models.CharField(max_length=50, blank=True, null=True, verbose_name="Estado")

    def __str__(self):
        return f"Oficina: {self.nome_fantasia} ({self.user.username})"

    class Meta:
        verbose_name = "Perfil de Oficina"
        verbose_name_plural = "Perfis de Oficinas"


# 🔹 Criar perfil automaticamente ao cadastrar usuário
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 'cliente':
            ClienteProfile.objects.create(user=instance)
        elif instance.user_type == 'oficina':
            OficinaProfile.objects.create(user=instance, nome_fantasia=instance.username)
