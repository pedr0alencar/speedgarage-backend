from django.db import models
from django.contrib.auth.models import User  # usando usuário padrão

class Carro(models.Model):
    marca  = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    ano    = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.marca} {self.modelo} {self.ano}"

class Critica(models.Model):
    usuario   = models.ForeignKey(User, on_delete=models.CASCADE, related_name='criticas')
    carro     = models.ForeignKey(Carro, on_delete=models.CASCADE, related_name='criticas')
    avaliacao = models.IntegerField()
    texto     = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.carro} - {self.avaliacao}★ by {self.usuario.username}"
