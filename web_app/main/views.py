from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, 'main/index.html')


def generate_items(request):
    return render(request, 'main/generator.html')


def profile(request):
    return render(request, 'main/profile.html')


def register(request):
    return render(request, 'main/register.html')


def login(request):
    return render(request, 'main/login.html')


def error_404(request):
    return render(request, 'main/404.html')
