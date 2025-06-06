import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from reviews.models import Carro, Critica

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def usuario_autenticado(db):
    """
    Cria e retorna um usuário, além de retornar token JWT de acesso.
    """
    user = User.objects.create_user(username="user1", password="senha123")
    # Obter token via login
    response = APIClient().post(
        "/api/token/",
        {"username": "user1", "password": "senha123"},
        format="json"
    )
    access = response.data.get("access")
    return {"user": user, "token": access}

@pytest.mark.django_db
def test_listar_carros_sem_token_retorna_401(api_client):
    """
    Quando não há credencial, GET /api/cars/ devolve 401 Unauthorized.
    """
    response = api_client.get("/api/cars/")
    assert response.status_code == 401

@pytest.mark.django_db
def test_listar_carros_com_token_retorna_200(api_client, usuario_autenticado):
    """
    Quando há credencial válida, GET /api/cars/ devolve 200 OK e lista vazia.
    """
    token = usuario_autenticado["token"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    response = api_client.get("/api/cars/")
    assert response.status_code == 200
    assert response.json() == []

@pytest.mark.django_db
def test_criar_carro_com_token(api_client, usuario_autenticado):
    """
    POST /api/cars/ com token válido deve criar e retornar o carro.
    """
    token = usuario_autenticado["token"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    data = {"marca": "Honda", "modelo": "Fit", "ano": 2009}
    response = api_client.post("/api/cars/", data, format="json")
    assert response.status_code == 201
    assert response.data["marca"] == "Honda"
    assert response.data["modelo"] == "Fit"
    assert response.data["ano"] == 2009

@pytest.mark.django_db
def test_listar_criticas_sem_token_retorna_200(api_client):
    """
    GET /api/reviews/ sem token deve devolver 200 OK e lista vazia.
    """
    response = api_client.get("/api/reviews/")
    assert response.status_code == 200
    assert response.json() == []

@pytest.mark.django_db
def test_criar_critica_com_token(api_client, usuario_autenticado):
    """
    POST /api/reviews/ com token válido cria uma crítica vinculada.
    """
    token = usuario_autenticado["token"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    # criar um carro antes (exige token)
    car_data = {"marca": "Subaru", "modelo": "Impreza", "ano": 2007}
    car_resp = api_client.post("/api/cars/", car_data, format="json")
    carro_id = car_resp.data["id"]

    # criar crítica apontando para esse carro
    review_data = {"carro": carro_id, "avaliacao": 4, "texto": "Muito bom."}
    review_resp = api_client.post("/api/reviews/", review_data, format="json")
    assert review_resp.status_code == 201
    assert review_resp.data["carro"] == carro_id
    assert review_resp.data["avaliacao"] == 4
    assert review_resp.data["texto"] == "Muito bom."

@pytest.mark.django_db
def test_editar_critica_somente_autor(api_client, usuario_autenticado):
    """
    Somente o usuário que criou a crítica pode editá-la.
    """
    token = usuario_autenticado["token"]
    user = usuario_autenticado["user"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    # criar carro e crítica
    car = Carro.objects.create(marca="Fiat", modelo="147", ano=1985)
    review = Critica.objects.create(usuario=user, carro=car, avaliacao=3, texto="Legal.")
    # editar com o mesmo usuário
    data_edit = {"carro": car.id, "avaliacao": 2, "texto": "Mudei de ideia."}
    response_ok = api_client.put(f"/api/reviews/{review.id}/", data_edit, format="json")
    assert response_ok.status_code == 200
    assert response_ok.data["avaliacao"] == 2

    # agora, outro usuário tenta editar (criar um usuário2)
    user2 = User.objects.create_user(username="user2", password="pass2")
    # obter token de user2
    resp2 = APIClient().post("/api/token/", {"username": "user2", "password": "pass2"}, format="json")
    token2 = resp2.data["access"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token2}")
    data_edit2 = {"carro": car.id, "avaliacao": 1, "texto": "Não posso."}
    response_forbidden = api_client.put(f"/api/reviews/{review.id}/", data_edit2, format="json")
    assert response_forbidden.status_code == 403

@pytest.mark.django_db
def test_excluir_critica_somente_autor(api_client, usuario_autenticado):
    """
    Somente o usuário que criou a crítica pode excluí-la.
    """
    token = usuario_autenticado["token"]
    user = usuario_autenticado["user"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    # criar carro e crítica
    car = Carro.objects.create(marca="Ford", modelo="Ka", ano=2010)
    review = Critica.objects.create(usuario=user, carro=car, avaliacao=2, texto="Ok.")
    # excluir com o mesmo usuário
    response_ok = api_client.delete(f"/api/reviews/{review.id}/")
    assert response_ok.status_code == 204

    # criar nova crítica para testar usuário2
    review2 = Critica.objects.create(usuario=user, carro=car, avaliacao=3, texto="Ainda ok.")
    # tentar excluir com user2
    user2 = User.objects.create_user(username="user3", password="pass3")
    resp2 = APIClient().post("/api/token/", {"username": "user3", "password": "pass3"}, format="json")
    token2 = resp2.data["access"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token2}")
    response_forbidden = api_client.delete(f"/api/reviews/{review2.id}/")
    assert response_forbidden.status_code == 403
