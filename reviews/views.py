# reviews/views.py
from rest_framework import viewsets, permissions, filters
from django.db.models import Avg
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
from rest_framework.decorators import action
from rest_framework.response import Response


class CarroViewSet(viewsets.ModelViewSet):
    queryset = Carro.objects.all().annotate(media_avaliacao=Avg('criticas__avaliacao'))
    serializer_class = CarroSerializer
    permission_classes = [permissions.IsAuthenticated]          # exige login
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ["marca", "modelo", "ano", "media_avaliacao"]
    ordering = ["-ano"]
    search_fields = ["marca", "modelo", "ano"]

    @action(detail=False, methods=['get'])
    def marcas(self, request):
        marcas = Carro.objects.values_list('marca', flat=True).distinct()
        return Response(marcas)

    @action(detail=False, methods=['get'])
    def modelos(self, request):
        marca = request.query_params.get('marca')
        if not marca:
            return Response({"error": "Parâmetro 'marca' é obrigatório."}, status=400)
        modelos = Carro.objects.filter(marca=marca).values_list('modelo', flat=True).distinct()
        return Response(modelos)

    @action(detail=False, methods=['get'])
    def anos(self, request):
        marca = request.query_params.get('marca')
        modelo = request.query_params.get('modelo')
        if not marca or not modelo:
            return Response({"error": "Parâmetros 'marca' e 'modelo' são obrigatórios."}, status=400)
        anos = Carro.objects.filter(marca=marca, modelo=modelo).values_list('ano', flat=True).distinct()
        return Response(anos)

    @action(detail=False, methods=['get'])
    def top(self, request):
        """
        Retorna os N carros com maior média de avaliação.
        Query param 'n' define quantos retornar (padrão 3).
        """
        try:
            n = int(request.query_params.get('n', 3))
        except ValueError:
            return Response({"error": "Parâmetro 'n' deve ser um inteiro."}, status=400)

        top_cars = (
            Carro.objects
            .annotate(media_avaliacao=Avg('critica__avaliacao'))
            .order_by('-media_avaliacao')[:n]
        )
        serializer = self.get_serializer(top_cars, many=True)
        return Response(serializer.data)


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
        my_param = self.request.query_params.get('my', '').lower()
        user = self.request.user

        print(f"[DEBUG] Query param: my={my_param}")
        print(f"[DEBUG] User: {user} ({type(user)}) - authenticated? {user.is_authenticated}")

        if my_param == 'true':
            if user.is_authenticated:
                qs = Critica.objects.filter(usuario=user).select_related("carro", "usuario")
                print(f"[DEBUG] Returning {qs.count()} reviews for user {user}")
                return qs
            else:
                print("[DEBUG] User is not authenticated.")
                return Critica.objects.none()

        return Critica.objects.select_related("carro", "usuario").all()   


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
