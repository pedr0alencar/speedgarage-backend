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
    usuario   = models.ForeignKey(User,  on_delete=models.CASCADE, related_name="criticas")
    carro     = models.ForeignKey(Carro, on_delete=models.CASCADE, related_name="criticas")
    avaliacao = models.IntegerField()
    texto     = models.TextField(max_length=2_000)
    criado_em = models.DateTimeField(auto_now_add=True)      # ← voltou

    class Meta:
        ordering = ["-criado_em"]

    def __str__(self):
        return f"{self.carro} – {self.avaliacao}★ by {self.usuario.username}"
