from django.contrib import admin
from .models import Carro, Critica, CarroImagem


@admin.register(Carro)
class CarroAdmin(admin.ModelAdmin):
    list_display = ("marca", "modelo", "ano")
    search_fields = ("marca", "modelo")


@admin.register(CarroImagem)
class CarroImagemAdmin(admin.ModelAdmin):
    list_display = ("carro", "tipo", "foto")
    list_filter  = ("tipo", "carro__marca")


@admin.register(Critica)
class CriticaAdmin(admin.ModelAdmin):
    list_display = ("carro", "usuario", "avaliacao", "criado_em")
    list_filter  = ("avaliacao", "carro__marca")
    search_fields = ("carro__modelo", "usuario__username")
