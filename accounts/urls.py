from django.urls import path, include
from knox import views as knox_views
# from accounts import views
from .views import *
from rest_framework_simplejwt.views import TokenVerifyView,TokenObtainPairView

urlpatterns = [
    path('register/', RegisterAPI.as_view(), name='register'),
    path('login/', LoginAPI.as_view(), name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path('register-token/', RegisterUserAPI.as_view(), name='register-token'),
    path('register-api/', UserRegisterAPIView.as_view(), name='register-api'),
    path('user-login/', UserLoginAPIView.as_view(), name='user-login'),
    path('user-logout/', UserLogoutAPIView.as_view(), name='user-logout'),
    # JWT token
    path('api/token/', TokenObtainPairView.as_view(), name='token'),
    path('api/token/refresh/', TokenVerifyView.as_view(), name='token_verify'),
    path('jwt-login/', UserJWTLogin.as_view(), name='jwt-login'),
    path('jwt-register/', JWTRegisterAPIView.as_view(), name='jwt-register'),

]
