from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db import IntegrityError
from .models import *


def index(request):
    return render(request, "base/index.html")

def cardapio(request):
    return render(request, "base/cardapio.html")

def categorias(request):
    return render(request, "base/categorias.html")

def sobre(request):
    return render(request, "base/sobre.html")

def login_view(request):
    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user != None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))

        else:
            return render(request, "base/login.html", {
                "error": "Nome ou senha inválidos. Tente novamente."
            })
    else:
        return render(request, "base/login.html")
        

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    if request.method == "POST":

        #Pega todos os campos
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        #Verifica a senha
        if password != confirmation:
            return render(request, "base/register.html", {
                "error": "As senhas devem ser iguais"
            })
        #Tenta criar um novo usuario
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "base/register.html", {
                "error": "Este usuário já existe"
            })
        #Loga o usuario
        login(request, user)
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, "base/register.html")
