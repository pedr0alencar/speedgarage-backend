# reviews/tests/conftest.py
import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.fixture
def api_client():
    """DRF APIClient sem autenticação."""
    return APIClient()


@pytest.fixture
def usuario_autenticado(db):
    """
    Cria um usuário, devolve dict com o User e o token JWT de acesso.
    Uso:
        token = usuario_autenticado["token"]
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    """
    User = get_user_model()
    user = User.objects.create_user(
        username="user1",
        email="user1@example.com",
        password="senha123",
    )
    refresh = RefreshToken.for_user(user)
    return {"user": user, "token": str(refresh.access_token)}
