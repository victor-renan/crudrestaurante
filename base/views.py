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
    cardapio = Prato.objects.order_by('-data').all()
    categorias = Categoria.objects.all()
    encomendas = Encomenda.objects.filter(user=request.user).all()
    pratos_encomendados = []

    for encomenda in encomendas:
        pratos_encomendados.append(encomenda.prato.id)

    #Verifica se o metodo eh POST
    if request.method == "POST":
        if request.user.is_admin():
            deletar_prato = request.POST.get("deletar_prato")

            if deletar_prato:
                Prato.objects.get(pk=deletar_prato).delete()

            nome = request.POST.get("nome_prato")
            descricao = request.POST.get("descricao_prato")
            categoria = request.POST.get("categoria_prato")
            imagem = request.POST.get("imagem_prato")

            if nome and descricao and categoria and imagem:
                Prato.objects.create(
                    nome=nome,
                    descricao=descricao,
                    categoria=Categoria.objects.get(pk=categoria),
                    imagem=imagem
                ).save()
        else:
            encomenda = request.POST["encomenda"]
            quantidade = request.POST["quantidade"]

            #verifica se o input foi repassado
            if encomenda and quantidade:
                Encomenda.objects.create(
                    user=request.user,
                    prato=Prato.objects.filter(id=encomenda).get(),
                    quantidade=quantidade
                ).save()
        #Recarrega a via GET
        return HttpResponseRedirect(reverse('cardapio'))

    #Verifica a form do filtro enviou a querry
    filtro = request.GET.get("filtro")
    if filtro:
        if filtro != 'Todos':
            cardapio = Prato.objects.filter(categoria__nome=filtro)

    #Carrega a pagina
    return render(request, "base/cardapio.html", {
        "cardapio": cardapio,
        "categorias": categorias,
        "encomendas": encomendas,
        "pratos_encomendados": pratos_encomendados,
        "admin": request.user.is_admin()
    })

def prato(request, prato_id):
    if request.method == "POST":
        nome = request.POST["nome_prato"]
        descricao = request.POST["descricao_prato"]
        categoria = request.POST["categoria_prato"]
        imagem = request.POST["imagem_prato"]

        if nome and descricao and categoria and imagem:
            Prato.objects.filter(pk=prato_id).update(
                nome=nome,
                descricao=descricao,
                categoria=Categoria.objects.get(pk=categoria),
                imagem=imagem
            )

            return HttpResponseRedirect(reverse('cardapio'))

    return render(request, "base/prato.html", {
        "prato": Prato.objects.get(pk=prato_id),
        "admin": request.user.is_admin(),
        "categorias": Categoria.objects.all()
    })

def categorias(request):
    return render(request, "base/categorias.html", {
        "categorias": Categoria.objects.all()
    })


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
