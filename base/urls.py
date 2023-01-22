from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("cardapio/",  views.cardapio, name="cardapio"),
    path("cardapio/prato/<int:prato_id>", views.prato, name="prato"),
    path("categorias/",  views.categorias, name="categorias"),
    path("sobre/",  views.sobre, name="sobre"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
]