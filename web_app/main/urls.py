from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path('generate', views.generate_items, name='generator'),
    path('profile', views.profile, name='profile'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('error', views.error_404, name='error'),


    path('index_beauty', views.beauty, name='beauty'),
    path('index_products', views.products, name='products'),
    path('index_parfum', views.activity, name='activity'),
    path('index_activity', views.parfum, name='parfum'),
    path('index_it', views.it, name='it'),


    path('gen_b', views.gen_b, name='gen_b'),
    path('gen_p', views.gen_p, name='gen_p'),
    path('gen_parf', views.gen_parf, name='gen_parf'),
    path('gen_act', views.gen_act, name='gen_act'),
    path('gen_it', views.gen_it, name='gen_it'),
]
