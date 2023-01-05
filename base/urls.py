from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("cardapio/",  views.sobre, name="cardapio"),
    path("categorias/",  views.categorias, name="categorias"),
    path("sobre/",  views.sobre, name="sobre"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
]