from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("O e-mail é obrigatório")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)

    USER_TYPE_CHOICES = (
        ('cliente', 'Cliente'),
        ('oficina', 'Oficina'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='cliente')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return f"{self.email} ({self.get_user_type_display()})"


class ClienteProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cliente_profile")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefone")
    cpf = models.CharField(max_length=20, blank=True, null=True, unique=True, verbose_name="CPF")
    data_nascimento = models.DateField(null=True, blank=True, verbose_name="Data de Nascimento")
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name="Cidade")
    state = models.CharField(max_length=50, blank=True, null=True, verbose_name="Estado")

    def __str__(self):
        return f"Cliente: {self.user.email}"

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
        return f"Oficina: {self.nome_fantasia} ({self.user.email})"

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
            OficinaProfile.objects.create(user=instance, nome_fantasia=instance.email)
