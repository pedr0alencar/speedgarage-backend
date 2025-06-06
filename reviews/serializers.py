from rest_framework import serializers
from .models import Carro, Critica

class CarroSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Carro
        fields = "__all__"


class CriticaSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Critica
        # Apenas os campos básicos: carro, avaliacao, texto, criado_em
        fields = ["id", "carro", "avaliacao", "texto", "criado_em"]
        read_only_fields = ["usuario", "criado_em"]

    def create(self, validated_data):
        # Garante que o 'usuario' seja o usuário logado
        return Critica.objects.create(
            usuario=self.context["request"].user,
            **validated_data
        )
