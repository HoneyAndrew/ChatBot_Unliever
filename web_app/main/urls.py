from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path('generate', views.generate_items, name='generator'),
    path('profile', views.profile, name='profile'),
    path('login', views.login, name='login'),
    path('login', views.register, name='register'),
    path('error', views.error_404, name='error'),
]
