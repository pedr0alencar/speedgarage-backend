from django.db import models
from django.contrib.auth.models import User

class Carro(models.Model):
    marca  = models.CharField("Marca",  max_length=40, default='Desconhecida')
    modelo = models.CharField("Modelo", max_length=40)
    ano    = models.PositiveIntegerField("Ano")

    class Meta:
        unique_together = ("marca", "modelo", "ano")
        ordering = ["marca", "modelo", "-ano"]

    def __str__(self):
        return f"{self.marca} {self.modelo} {self.ano}"


class Critica(models.Model):
    usuario   = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="criticas",
        verbose_name="Usuário"
    )
    carro     = models.ForeignKey(
        Carro,
        on_delete=models.CASCADE,
        related_name="criticas",
        verbose_name="Carro"
    )
    avaliacao = models.IntegerField("Avaliação (1 a 5)")
    texto     = models.TextField("Texto da crítica", max_length=2000)
    criado_em = models.DateTimeField("Data de criação", auto_now_add=True)

    class Meta:
        ordering = ["-criado_em"]
        verbose_name = "Crítica"
        verbose_name_plural = "Críticas"

    def __str__(self):
        return f"{self.carro} – {self.avaliacao}★ por {self.usuario.username}"
