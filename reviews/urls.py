from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    CarroImagemViewSet,
    CarroViewSet,
    CriticaViewSet,
    RegisterView,
    CustomTokenObtainPairView,
)

router = DefaultRouter()
router.register(r'cars', CarroViewSet, basename='carro')
router.register(r'reviews', CriticaViewSet, basename='critica')
router.register(r'car-images', CarroImagemViewSet, basename='carroimagem')

urlpatterns = [
    # endpoints CRUD + actions (marcas, modelos, anos, top)
    path('', include(router.urls)),

    # registro de usuário
    path('register/', RegisterView.as_view(), name='register'),

    # JWT
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
