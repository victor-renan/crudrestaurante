from django.contrib import admin
from .models import User, Prato, Categoria

admin.site.register(User)
admin.site.register(Prato)
admin.site.register(Categoria)