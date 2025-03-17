from django.contrib import admin
from django.urls import path, include
from news.views import CreateUserView
from rest_framework_simplejwt.views import TokenRefreshView
from news.views import CustomTokenObtainPairView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/user/register/', CreateUserView.as_view(), name='create_user'),
    path("api-auth/", include("rest_framework.urls")),
    path('api/',include('news.urls')),
]
