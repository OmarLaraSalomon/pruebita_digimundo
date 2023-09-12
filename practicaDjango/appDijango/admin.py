from django.contrib import admin
from .models import CategoriaProd, Productos, Servicios, Pedido, LineaPedido, Noticias
# Register your models here.

class CategoriaProdAdmin(admin.ModelAdmin):

    readonly_fields=("created","update")


class ProductoAdmin(admin.ModelAdmin):

    readonly_fields=("created","update")

   

class ServicioAdmin(admin.ModelAdmin):

    readonly_fields=("created","update")



class NoticiaAdmin(admin.ModelAdmin):

    readonly_fields=("created","update")


class LineaAdmin(admin.ModelAdmin):
    list_display=("id","cantidad",)



class PedidoAdmin(admin.ModelAdmin):
    list_display=("id","user",)
   




admin.site.register(CategoriaProd, CategoriaProdAdmin)

admin.site.register(Productos, ProductoAdmin)

admin.site.register(Noticias, NoticiaAdmin)

admin.site.register(Servicios, ServicioAdmin)

admin.site.register(LineaPedido,LineaAdmin)

admin.site.register(Pedido,PedidoAdmin)


