from rest_framework import serializers
from .models import Carro, Critica
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from rest_framework import serializers

class CarroSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Carro
        fields = "__all__"


class CriticaSerializer(serializers.ModelSerializer):
    usuario_nome = serializers.SerializerMethodField()
    carro_nome = serializers.SerializerMethodField()
    class Meta:
        model  = Critica
        # Apenas os campos básicos: carro, avaliacao, texto, criado_em
        fields = ["id", "usuario_nome","carro_nome", "avaliacao", "texto", "criado_em"]
        read_only_fields = ["usuario", "criado_em"]
        
    def get_usuario_nome(self, obj):
        return obj.usuario.username  

    def get_carro_nome(self, obj):
        return obj.carro.modelo 

    def create(self, validated_data):
        # Garante que o 'usuario' seja o usuário logado
        return Critica.objects.create(
            usuario=self.context["request"].user,
            **validated_data
        )


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # Permite login com email ou username
        attrs['username'] = attrs.get('email', attrs.get('username'))
        return super().validate(attrs)
    
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # Aceita username ou email
        username_or_email = attrs.get('username')
        password = attrs.get('password')

        if '@' in username_or_email:
            try:
                user = User.objects.get(email=username_or_email)
                attrs['username'] = user.username  # Substitui pelo username real
            except User.DoesNotExist:
                pass
                
        return super().validate(attrs)