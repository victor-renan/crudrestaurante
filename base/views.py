from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required

from .models import *


def index(request):
    return render(request, "base/index.html")


@login_required(login_url='/login/')
def cardapio(request):
    #SELECT * FROM x
    cardapio = Prato.objects.all()
    categorias = Categoria.objects.all()
    encomendas = Encomenda.objects.filter(user=request.user).all()
    pratos_encomendados = []

    for encomenda in encomendas:
        pratos_encomendados.append(encomenda.prato.id)

    #Define o contexto
    context = {
        "cardapio": cardapio,
        "categorias": categorias,
        "encomendas": encomendas,
        "pratos_encomendados": pratos_encomendados
    }
    #Verifica se o metodo eh POST
    if request.method == "POST": 
        encomenda = request.POST["encomenda"]
        quantidade = request.POST["quantidade"]

        #verifica se o input foi repassado
        if encomenda:
            Encomenda.objects.create(
                user=request.user,
                prato=Prato.objects.filter(id=encomenda).get(),
                quantidade=quantidade
            ).save()
        
        #Refresh the values
        cardapio = Prato.objects.all()
        categorias = Categoria.objects.all()
        encomendas = Encomenda.objects.filter(user=request.user).all()
        pratos_encomendados = []

        for encomenda in encomendas:
            pratos_encomendados.append(encomenda.prato.id)

        #atualiza o contexto
        context.update({"message": "A encomenda foi feita com sucesso!"})

        return render(request, "base/cardapio.html", context)

    #Verifica a form do filtro enviou a querry
    filtro = request.GET.get("filtro")
    if filtro:
        if filtro != 'Todos':
            cardapio = Prato.objects.filter(categoria__nome=filtro)

    #Carrega a pagina
    return render(request, "base/cardapio.html", context)


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
