from django.contrib import admin
from .models import CategoriaProd, Productos, Servicios
# Register your models here.

class CategoriaProdAdmin(admin.ModelAdmin):

    readonly_fields=("created","update")


class ProductoAdmin(admin.ModelAdmin):

    readonly_fields=("created","update")

   

class ServicioAdmin(admin.ModelAdmin):

    readonly_fields=("created","update")



admin.site.register(CategoriaProd, CategoriaProdAdmin)

admin.site.register(Productos, ProductoAdmin)

admin.site.register(Servicios, ServicioAdmin)


