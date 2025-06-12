import pytest
from django.contrib.auth.models import User
from reviews.models import Carro, Critica


# --------------------------------------------------------------------------------------
# LISTAGEM / CRUD DE CARROS
# --------------------------------------------------------------------------------------

@pytest.mark.django_db
def test_listar_carros_sem_token_retorna_401(api_client):
    response = api_client.get("/api/cars/")
    assert response.status_code == 401


@pytest.mark.django_db
def test_listar_carros_com_token_retorna_200(api_client, usuario_autenticado):
    token = usuario_autenticado["token"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    response = api_client.get("/api/cars/")
    assert response.status_code == 200
    assert response.data["count"] == 0
    assert response.data["results"] == []


@pytest.mark.django_db
def test_criar_carro_com_token(api_client, usuario_autenticado):
    token = usuario_autenticado["token"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    data = {"marca": "Toyota", "modelo": "Corolla", "ano": 2020}
    resp_create = api_client.post("/api/cars/", data, format="json")
    assert resp_create.status_code == 201

    resp_list = api_client.get("/api/cars/")
    assert resp_list.data["count"] == 1
    carro = resp_list.data["results"][0]
    assert carro["marca"] == "Toyota"
    assert carro["modelo"] == "Corolla"
    assert carro["ano"] == 2020


@pytest.mark.django_db
def test_editar_carro(api_client, usuario_autenticado):
    token = usuario_autenticado["token"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    carro = Carro.objects.create(marca="Honda", modelo="Civic", ano=2018)

    data_edit = {"marca": "Honda", "modelo": "Civic", "ano": 2025}
    resp_edit = api_client.put(f"/api/cars/{carro.id}/", data_edit, format="json")
    assert resp_edit.status_code == 200
    assert resp_edit.data["ano"] == 2025


@pytest.mark.django_db
def test_deletar_carro(api_client, usuario_autenticado):
    token = usuario_autenticado["token"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    carro = Carro.objects.create(marca="Renault", modelo="Sandero", ano=2015)
    resp_delete = api_client.delete(f"/api/cars/{carro.id}/")
    assert resp_delete.status_code == 204
    assert not Carro.objects.filter(id=carro.id).exists()


@pytest.mark.django_db
def test_carro_duplicado(api_client, usuario_autenticado):
    token = usuario_autenticado["token"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    data = {"marca": "Fiat", "modelo": "Uno", "ano": 2010}
    assert api_client.post("/api/cars/", data, format="json").status_code == 201
    resp_dup = api_client.post("/api/cars/", data, format="json")
    assert resp_dup.status_code in (400, 500)


# --------------------------------------------------------------------------------------
# LISTAGEM / CRUD DE CRÍTICAS
# --------------------------------------------------------------------------------------

@pytest.mark.django_db
def test_listar_criticas_sem_token_retorna_200(api_client):
    resp = api_client.get("/api/reviews/")
    assert resp.status_code == 200
    assert resp.data["count"] == 0
    assert resp.data["results"] == []


@pytest.mark.django_db
def test_criar_critica_sem_token(api_client):
    carro = Carro.objects.create(marca="VW", modelo="Gol", ano=2022)
    resp = api_client.post("/api/reviews/", {"carro": carro.id, "avaliacao": 4, "texto": "Sem auth"}, format="json")
    assert resp.status_code == 401


@pytest.mark.django_db
def test_criar_critica_com_token(api_client, usuario_autenticado):
    token = usuario_autenticado["token"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    carro = Carro.objects.create(marca="Subaru", modelo="Impreza", ano=2007)
    resp = api_client.post("/api/reviews/", {"carro": carro.id, "avaliacao": 4, "texto": "Muito bom."}, format="json")
    assert resp.status_code == 201


@pytest.mark.django_db
def test_detalhar_critica(api_client, usuario_autenticado):
    token = usuario_autenticado["token"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    carro = Carro.objects.create(marca="Ford", modelo="Ka", ano=2022)
    resp = api_client.post("/api/reviews/", {"carro": carro.id, "avaliacao": 5, "texto": "Detalhe"}, format="json")
    critica_id = resp.data["id"]

    api_client.credentials()  # remove token
    resp_det = api_client.get(f"/api/reviews/{critica_id}/")
    assert resp_det.status_code == 200
    assert resp_det.data["texto"] == "Detalhe"


@pytest.mark.django_db
def test_busca_por_criticas(api_client, usuario_autenticado):
    token = usuario_autenticado["token"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    c1 = Carro.objects.create(marca="Fiat", modelo="Uno", ano=2010)
    c2 = Carro.objects.create(marca="Ford", modelo="Ka", ano=2022)

    api_client.post("/api/reviews/", {"carro": c1.id, "avaliacao": 4, "texto": "Ótimo desempenho"}, format="json")
    api_client.post("/api/reviews/", {"carro": c2.id, "avaliacao": 3, "texto": "Consome pouco"}, format="json")

    api_client.credentials()
    assert api_client.get("/api/reviews/?search=desempenho").data["count"] == 1
    assert api_client.get("/api/reviews/?search=Ka").data["count"] == 1


@pytest.mark.django_db
def test_avaliacao_fora_do_intervalo(api_client, usuario_autenticado):
    token = usuario_autenticado["token"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    carro = Carro.objects.create(marca="Chevrolet", modelo="Onix", ano=2021)

    resp = api_client.post("/api/reviews/", {"carro": carro.id, "avaliacao": 0, "texto": "Inválida"}, format="json")
    assert resp.status_code == 400
    resp = api_client.post("/api/reviews/", {"carro": carro.id, "avaliacao": 6, "texto": "Inválida"}, format="json")
    assert resp.status_code == 400


@pytest.mark.django_db
def test_editar_critica_somente_autor(api_client, usuario_autenticado):
    token = usuario_autenticado["token"]
    user = usuario_autenticado["user"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    carro = Carro.objects.create(marca="Fiat", modelo="147", ano=1985)
    review = Critica.objects.create(usuario=user, carro=carro, avaliacao=3, texto="Legal")

    resp_ok = api_client.put(f"/api/reviews/{review.id}/", {"carro": carro.id, "avaliacao": 2, "texto": "Mudou"}, format="json")
    assert resp_ok.status_code == 200

    other = User.objects.create_user("user2", password="pass2")
    other_token = api_client.post("/api/token/", {"username": "user2", "password": "pass2"}).data["access"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {other_token}")
    resp_forbidden = api_client.put(f"/api/reviews/{review.id}/", {"carro": carro.id, "avaliacao": 1, "texto": "x"}, format="json")
    assert resp_forbidden.status_code == 403


@pytest.mark.django_db
def test_excluir_critica_somente_autor(api_client, usuario_autenticado):
    token = usuario_autenticado["token"]
    user = usuario_autenticado["user"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    carro = Carro.objects.create(marca="VW", modelo="Fusca", ano=1972)
    review = Critica.objects.create(usuario=user, carro=carro, avaliacao=5, texto="Top!")

    assert api_client.delete(f"/api/reviews/{review.id}/").status_code == 204

    review2 = Critica.objects.create(usuario=user, carro=carro, avaliacao=1, texto="Ruim")
    other = User.objects.create_user("user3", password="pass3")
    other_token = api_client.post("/api/token/", {"username": "user3", "password": "pass3"}).data["access"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {other_token}")
    assert api_client.delete(f"/api/reviews/{review2.id}/").status_code == 403
