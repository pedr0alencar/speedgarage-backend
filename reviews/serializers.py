from rest_framework import serializers
from .models import Carro, Critica
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from rest_framework import serializers

class CarroSerializer(serializers.ModelSerializer):
    media_avaliacao = serializers.FloatField(read_only=True)
    class Meta:
        model  = Carro
        fields = "__all__"


class CriticaSerializer(serializers.ModelSerializer):
    usuario_nome = serializers.SerializerMethodField()
    carro_nome = serializers.SerializerMethodField()
    total_likes = serializers.IntegerField(
        source='liked_users.count',
        read_only=True
    )
    liked_by_me = serializers.SerializerMethodField()
    class Meta:
        model  = Critica
        # Apenas os campos básicos: carro, avaliacao, texto, criado_em
        fields = ["id", "carro",  # ← novo
                 "usuario_nome", "carro_nome",
                 "avaliacao", "texto", "criado_em",  "total_likes"]
        read_only_fields = ["usuario", "criado_em"]
        extra_kwargs = {
            "carro": {"write_only": True}
        }

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

    def validate_avaliacao(self, value):
        if not 1 <= value <= 5:
            raise serializers.ValidationError("A avaliação deve ser entre 1 e 5.")
        return value

    def get_liked_by_me(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return obj.liked_users.filter(pk=user.pk).exists()
        return False


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
        # Pega o campo que o usuário enviou como 'username' no Angular
        username_or_email = attrs.get('username')
        password = attrs.get('password')

        # lógica para permitir login com email (que está ótima)
        if '@' in username_or_email:
            try:
                # Encontra o usuário pelo email
                user = User.objects.get(email__iexact=username_or_email) 
                # Substitui o email pelo username correspondente para a autenticação padrão
                attrs['username'] = user.username
            except User.DoesNotExist:
                # Se não encontrar, a validação padrão abaixo irá falhar, o que é o esperado
                pass
        
        # 1. Chama o metodo original para obter os tokens
        # Ele autentica o usuário e retorna {'access': '...', 'refresh': '...'}
        data = super().validate(attrs)
        
        # 2. Adiciona os dados do usuário à resposta
        # Após a validação, `self.user` contém o objeto do usuário logado
        data['user'] = {
            'id': self.user.id,
            'username': self.user.username,
            'email': self.user.email
        }
        
        # 3. Retorna o dicionário completo: tokens + dados do usuário
        return data