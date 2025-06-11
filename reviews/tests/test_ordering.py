import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from reviews.models import Carro, Critica

@pytest.mark.django_db
def test_ordering_carros(api_client: APIClient, usuario_autenticado):
    token = usuario_autenticado["token"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    Carro.objects.bulk_create([
        Carro(marca="X", modelo="A", ano=2015),
        Carro(marca="X", modelo="B", ano=1999),
        Carro(marca="X", modelo="C", ano=2020),
    ])

    resp = api_client.get("/api/cars/?ordering=ano")
    anos = [item["ano"] for item in resp.data["results"]]
    assert anos == [1999, 2015, 2020]           # ascendente

    resp = api_client.get("/api/cars/?ordering=-ano")
    anos = [item["ano"] for item in resp.data["results"]]
    assert anos == [2020, 2015, 1999]           # descendente

@pytest.mark.django_db
def test_ordering_reviews(api_client: APIClient, usuario_autenticado):
    token = usuario_autenticado["token"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    carro = Carro.objects.create(marca="X", modelo="Y", ano=2000)
    user  = usuario_autenticado["user"]
    Critica.objects.create(usuario=user, carro=carro, avaliacao=3, texto="ok")
    Critica.objects.create(usuario=user, carro=carro, avaliacao=5, texto="top")

    resp = api_client.get("/api/reviews/?ordering=-avaliacao")
    notas = [item["avaliacao"] for item in resp.data["results"]]
    assert notas == [5, 3]
