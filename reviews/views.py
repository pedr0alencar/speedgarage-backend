from rest_framework import viewsets, permissions, filters
from rest_framework.exceptions import PermissionDenied
from .models import Carro, Critica
from .serializers import CarroSerializer, CriticaSerializer


class CarroViewSet(viewsets.ModelViewSet):
    queryset = Carro.objects.all()
    serializer_class = CarroSerializer
    permission_classes = [permissions.IsAuthenticated]   # ← exige token para qualquer método
    filter_backends = [filters.SearchFilter]
    search_fields = ["marca", "modelo", "ano"]


class CriticaViewSet(viewsets.ModelViewSet):
    queryset = Critica.objects.select_related("carro", "usuario")
    serializer_class = CriticaSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ["carro__marca", "carro__modelo", "texto"]

    # Somente o autor pode editar/excluir
    def perform_update(self, serializer):
        if self.request.user != self.get_object().usuario:
            raise PermissionDenied("Apenas o autor pode editar.")
        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user != instance.usuario:
            raise PermissionDenied("Apenas o autor pode excluir.")
        instance.delete()
