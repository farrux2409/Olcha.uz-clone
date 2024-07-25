from django.urls import path, include
from knox import views as knox_views
# from accounts import views
from .views import *

urlpatterns = [
    path('register/', RegisterAPI.as_view(), name='register'),
    path('login/', LoginAPI.as_view(), name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path('register-token/', RegisterUserAPI.as_view(), name='register-token'),

]
