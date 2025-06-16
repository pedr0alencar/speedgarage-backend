from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import CarroViewSet, CriticaViewSet, RegisterView

router = DefaultRouter()
router.register(r'cars', CarroViewSet, basename='carro')
router.register(r'reviews', CriticaViewSet, basename='critica')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
]