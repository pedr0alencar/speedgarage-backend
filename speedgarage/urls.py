from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from reviews.views import CustomTokenObtainPairView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('reviews.urls')),  # Todas as rotas do app estarão em /api/...
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),  # JWT aqui
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
