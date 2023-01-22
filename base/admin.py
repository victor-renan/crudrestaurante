from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *

# Custom admin
class UserAdmin(BaseUserAdmin):
    pass

admin.site.register(User, UserAdmin)

# Demais models
admin.site.register(Prato)
admin.site.register(Categoria)
admin.site.register(Encomenda)