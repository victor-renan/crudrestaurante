from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

#Tabela para os pratos do cardápio
class Prato(models.Model):
    nome = models.CharField(max_length=64)
    categoria = models.ForeignKey('Categoria', on_delete=models.CASCADE)
    descricao = models.TextField(default=None)
    imagem = models.CharField(max_length=600, default=None)
    data = models.DateField(auto_now=True)
    def __str__(self):
        return f"{self.nome}, {self.data}"

#Tabela para as categorias
class Categoria(models.Model):
    nome = models.CharField(max_length=64)
    def __str__(self):
        return f"{self.nome}"