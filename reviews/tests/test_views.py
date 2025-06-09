import pytest
from django.contrib.auth.models import User
from reviews.models import Carro, Critica


# --------------------------------------------------------------------------------------
# LISTAGEM DE CARROS
# --------------------------------------------------------------------------------------

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

    # ---------- PAGINAÇÃO ----------
    assert response.data["count"] == 0
    assert response.data["results"] == []


@pytest.mark.django_db
def test_criar_carro_com_token(api_client, usuario_autenticado):
    """
    POST /api/cars/ com token válido cria um novo carro.
    """
    token = usuario_autenticado["token"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    data = {"marca": "Toyota", "modelo": "Corolla", "ano": 2020}
    resp_create = api_client.post("/api/cars/", data, format="json")
    assert resp_create.status_code == 201

    # Depois da criação deve haver exatamente 1 carro
    resp_list = api_client.get("/api/cars/")
    assert resp_list.data["count"] == 1
    carro = resp_list.data["results"][0]
    assert carro["marca"] == "Toyota"
    assert carro["modelo"] == "Corolla"
    assert carro["ano"] == 2020


# --------------------------------------------------------------------------------------
# LISTAGEM / CRUD DE CRÍTICAS
# --------------------------------------------------------------------------------------

@pytest.mark.django_db
def test_listar_criticas_sem_token_retorna_200(api_client):
    """
    GET /api/reviews/ sem token deve devolver 200 OK e lista vazia.
    A listagem de críticas é pública, mas paginada.
    """
    response = api_client.get("/api/reviews/")
    assert response.status_code == 200

    # ---------- PAGINAÇÃO ----------
    assert response.data["count"] == 0
    assert response.data["results"] == []


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
    # o serializer não devolve o campo 'usuario'; basta checar 201


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

    # ---------- tenta editar com outro usuário ----------
    other = User.objects.create_user("user2", password="pass2")
    other_token = api_client.post(
        "/api/token/", {"username": "user2", "password": "pass2"}
    ).data["access"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {other_token}")
    response_forbidden = api_client.put(
        f"/api/reviews/{review.id}/", data_edit, format="json"
    )
    assert response_forbidden.status_code == 403


@pytest.mark.django_db
def test_excluir_critica_somente_autor(api_client, usuario_autenticado):
    """
    Somente o autor pode deletar sua crítica.
    """
    token = usuario_autenticado["token"]
    user = usuario_autenticado["user"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    # cria carro + crítica
    car = Carro.objects.create(marca="VW", modelo="Fusca", ano=1972)
    review = Critica.objects.create(usuario=user, carro=car, avaliacao=5, texto="Top!")

    # deleção pelo autor
    resp_del_ok = api_client.delete(f"/api/reviews/{review.id}/")
    assert resp_del_ok.status_code == 204

    # ---------- tenta deletar com outro usuário ----------
    review2 = Critica.objects.create(
        usuario=user, carro=car, avaliacao=1, texto="Ruim!"
    )
    other = User.objects.create_user("user3", password="pass3")
    other_token = api_client.post(
        "/api/token/", {"username": "user3", "password": "pass3"}
    ).data["access"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {other_token}")
    resp_del_forbidden = api_client.delete(f"/api/reviews/{review2.id}/")
    assert resp_del_forbidden.status_code == 403
