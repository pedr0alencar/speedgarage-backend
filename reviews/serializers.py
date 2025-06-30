from rest_framework import serializers
from .models import Carro, CarroImagem, Critica
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from rest_framework import serializers

class CarroSerializer(serializers.ModelSerializer):
    media_avaliacao = serializers.FloatField(read_only=True)
    imagens = serializers.SerializerMethodField()
    imagem = serializers.SerializerMethodField()  # novo campo

    class Meta:
        model = Carro
        fields = ["id", "marca", "modelo", "ano",
                  "media_avaliacao", "imagem", "imagens"]

    def get_imagens(self, obj):
        return [im.foto.url for im in obj.imagens.all()]

    def get_imagem(self, obj):
        img = obj.imagens.filter(tipo='EX').first() or obj.imagens.first()
        return img.foto.url if img else None




class CriticaSerializer(serializers.ModelSerializer):
    usuario_nome = serializers.SerializerMethodField()
    carro_nome = serializers.SerializerMethodField()
    carro_marca = serializers.SerializerMethodField()
    carro_ano = serializers.SerializerMethodField()
    carro_imagem = serializers.SerializerMethodField()
    total_likes = serializers.IntegerField(
        source='liked_users.count',
        read_only=True
    )
    liked_by_me = serializers.SerializerMethodField()

    class Meta:
        model  = Critica
        fields = [
            "id", "carro",
            "usuario_nome", "carro_nome", "carro_marca", "carro_ano", "carro_imagem",
            "avaliacao", "texto", "criado_em",
            "total_likes", "liked_by_me"
        ]
        read_only_fields = ["usuario", "criado_em"]
        extra_kwargs = {
            "carro": {"write_only": True}
        }

    def get_usuario_nome(self, obj):
        return obj.usuario.username
    
    def get_carro_marca(self, obj):
        return obj.carro.marca

    def get_carro_nome(self, obj):
        return obj.carro.modelo 
    
    def get_carro_ano(self, obj):
        return obj.carro.ano

    def get_carro_marca(self, obj):
        return obj.carro.marca

    def get_carro_ano(self, obj):
        return obj.carro.ano

    def create(self, validated_data):
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

    def get_carro_imagem(self, obj):
        img = obj.carro.imagens.filter(tipo='EX').first() or obj.carro.imagens.first()
        return img.foto.url if img else None


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
    
class CarroImagemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarroImagem
        fields = ["id", "carro", "tipo", "foto"]