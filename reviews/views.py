# reviews/views.py
from rest_framework import viewsets, permissions, filters
from rest_framework.exceptions import PermissionDenied
from .models import Carro, Critica
from .serializers import (
    CarroSerializer,
    CriticaSerializer,
    RegisterSerializer,
    EmailTokenObtainPairSerializer,
    CustomTokenObtainPairSerializer,
)
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView


class CarroViewSet(viewsets.ModelViewSet):
    queryset = Carro.objects.all()
    serializer_class = CarroSerializer
    permission_classes = [permissions.IsAuthenticated]          # exige login
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ["marca", "modelo", "ano"]  # ← campos permitidos
    ordering = ["-ano"]
    search_fields = ["marca", "modelo", "ano"]


class CriticaViewSet(viewsets.ModelViewSet):
    queryset = Critica.objects.select_related("carro", "usuario")
    serializer_class = CriticaSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ["avaliacao", "criado_em", "carro__ano"]
    ordering = ["-criado_em"]
    search_fields = ["carro__marca", "carro__modelo", "texto"]

    # NEW ➜ passa o request para o serializer
    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx["request"] = self.request
        return ctx

    # NEW ➜ garante autor correto (opção 1)
    # Você pode omitir se o serializer já salva usuario=request.user
    def perform_create(self, serializer):
        # o serializer vai cuidar de atribuir o usuário
        serializer.save()

    # Somente o autor pode editar/excluir
    def perform_update(self, serializer):
        if self.request.user != self.get_object().usuario:
            raise PermissionDenied("Apenas o autor pode editar.")
        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user != instance.usuario:
            raise PermissionDenied("Apenas o autor pode excluir.")
        instance.delete()

    def get_queryset(self):
        if self.action == 'list':
            return Critica.objects.filter(usuario=self.request.user).select_related("carro", "usuario")
        return super().get_queryset()



class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
