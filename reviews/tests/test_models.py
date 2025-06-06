import pytest
from django.contrib.auth.models import User
from reviews.models import Carro, Critica

@pytest.mark.django_db
def test_criar_carro_com_campos_obrigatorios():
    """
    Gera um Carro com marca, modelo e ano, e valida se __str__ funciona.
    """
    carro = Carro.objects.create(marca="Toyota", modelo="Supra", ano=1994)
    assert carro.id is not None
    assert str(carro) == "Toyota Supra 1994"

@pytest.mark.django_db
def test_criar_critica_relacionada_a_usuario_e_carro():
    """
    Gera um usuário, um carro e uma crítica atrelada a ambos;
    valida se campos obrigatórios e método __str__ estão corretos.
    """
    # 1. Criar usuário
    user = User.objects.create_user(username="testuser", password="senha123")
    # 2. Criar carro
    carro = Carro.objects.create(marca="Dodge", modelo="Challenger", ano=1970)
    # 3. Criar crítica
    critica = Critica.objects.create(
        usuario=user,
        carro=carro,
        avaliacao=5,
        texto="Clássico atemporal!"
    )
    assert critica.id is not None
    # Verifica formato de __str__ (usando “por” em Português)
    expected_str = f"{carro} – {critica.avaliacao}★ por {user.username}"
    assert str(critica) == expected_str

    # Verifica que campo criado_em foi preenchido (na criação)
    assert critica.criado_em is not None
