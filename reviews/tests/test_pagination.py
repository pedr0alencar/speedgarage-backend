# reviews/tests/test_pagination.py
import pytest
from reviews.models import Carro

@pytest.mark.django_db
def test_paginacao_carros(api_client, usuario_autenticado):
    """
    /api/cars/ deve paginar com limit=5 por padrão e
    aceitar os parâmetros ?limit=N&offset=M.
    """
    # Cria 12 carros
    for i in range(12):
        Carro.objects.create(marca="Marca", modelo=f"Modelo {i}", ano=2000+i)

    # autentica
    api_client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {usuario_autenticado['token']}"
    )

    # 1) Requisição default (sem parâmetros) → 5 resultados
    resp = api_client.get("/api/cars/")
    assert resp.status_code == 200
    assert resp.data["count"] == 12
    assert len(resp.data["results"]) == 5
    # urls next/previous devem existir
    assert resp.data["next"] is not None
    assert resp.data["previous"] is None

    # 2) limit=7, offset=7  → últimos 5 (=12-7) resultados
    resp2 = api_client.get("/api/cars/?limit=7&offset=7")
    assert resp2.status_code == 200
    assert len(resp2.data["results"]) == 5
    # next deve ser None, previous não-None
    assert resp2.data["next"] is None
    assert resp2.data["previous"] is not None
