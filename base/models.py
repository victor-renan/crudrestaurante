from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class User(AbstractUser):
    class Meta:
        permissions = [
            ("system_admin", "Pode modificar o cardapio")
        ]
    def is_admin(self):
        return self.has_perm('system_admin')


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

class Encomenda(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    prato = models.ForeignKey('Prato', on_delete=models.CASCADE)
    quantidade = models.IntegerField(default=1)
    data = models.DateField(auto_now=True)
    def __str__(self):
        return f"{self.user} Pediu {self.quantidade} {self.prato} em {self.data}"