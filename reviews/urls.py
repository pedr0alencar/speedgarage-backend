from rest_framework.routers import DefaultRouter
from .views import CarroViewSet, CriticaViewSet

router = DefaultRouter()
router.register(r'cars',    CarroViewSet,   basename='carro')
router.register(r'reviews', CriticaViewSet, basename='critica')

urlpatterns = router.urls
