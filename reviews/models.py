from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class Carro(models.Model):
    marca  = models.CharField("Marca",  max_length=40, default="Desconhecida")
    modelo = models.CharField("Modelo", max_length=40)
    ano    = models.PositiveIntegerField("Ano")

    class Meta:
        unique_together = ("marca", "modelo", "ano")
        ordering = ["marca", "modelo", "-ano"]

    def __str__(self):
        return f"{self.marca} {self.modelo} {self.ano}"


class CarroImagem(models.Model):
    EXTERIOR = "EX"
    INTERIOR = "IN"
    MOTOR    = "MO"
    TIPO_CHOICES = [
        (EXTERIOR, "Exterior"),
        (INTERIOR, "Interior"),
        (MOTOR,    "Motor"),
    ]

    carro = models.ForeignKey(
        Carro,
        on_delete=models.CASCADE,
        related_name="imagens",
        verbose_name="Carro",
    )
    tipo  = models.CharField(
        "Tipo",
        max_length=2,
        choices=TIPO_CHOICES,
    )
    foto  = models.ImageField(
        "Foto",
        upload_to="carros",          # caminho lógico em Cloudinary
    )

    class Meta:
        unique_together = ("carro", "tipo")   # máx. 1 imagem de cada tipo
        ordering = ["carro", "tipo"]
        verbose_name = "Imagem de carro"
        verbose_name_plural = "Imagens de carro"

    def __str__(self):
        return f"{self.carro} · {self.get_tipo_display()}"


class Critica(models.Model):
    usuario   = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="criticas",
        verbose_name="Usuário",
    )
    carro     = models.ForeignKey(
        Carro,
        on_delete=models.CASCADE,
        related_name="criticas",
        verbose_name="Carro",
    )
    avaliacao = models.IntegerField("Avaliação (1 a 5)")
    texto     = models.TextField("Texto da crítica", max_length=2_000)
    criado_em = models.DateTimeField("Data de criação", auto_now_add=True)

    class Meta:
        ordering = ["-criado_em"]
        verbose_name = "Crítica"
        verbose_name_plural = "Críticas"

    def __str__(self):
        return f"{self.carro} – {self.avaliacao}★ por {self.usuario.username}"

    liked_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='liked_reviews',
        blank=True,
    )
