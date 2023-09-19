from django.urls import path
from . import views

from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path , re_path ,include

urlpatterns = [
    path('', views.feed, name ="feed"),
    url('^perfil/$' , views.perfil, name="perfil"),
    url('^layout/$' , views.layout, name="layout"),
    url('^register/$' , views.registro, name="registro"),
    url('^login/$' , LoginView.as_view(template_name='social/login.html'), name="login"),
    url('^logout/$' , LogoutView.as_view(template_name='social/logout.html'), name="logout"),
    url('^acceso/$' , views.retorno, name="pruebita"),
    url('^registro/$' , views.contactosregistro, name="contactosregistro"),
    url('^consulta/$' , views.consultar, name="consultas"),
    url('^carru/$' , views.carrusel, name="carrusel"),
    url('^correo/$' , views.mandarcorreo, name="mandarcorreo"),
    url('^consultarcorreo/$' , views.consultarc, name="consultarc"),
    url('^tienda/$' , views.tiendita, name="tiendita"),
    url('^productos/$' , views.produ, name="productos"),
    url('^servicio/$' , views.servi, name="servicios"),
    url('^home/$' , views.home, name="home"),
    url('^paginacion/$' , views.paginacion, name="paginacion"),
    url('^actualizar/$' , views.actualiza, name="actualizar"),
   
    url('procesar_pedido/', views.procesar_pedido, name="procesar_pedido"),

    path('', views.enviar_mail, name="enviar_email"),

   
# agregar  producto

  #este checa si exsite
    path('agregar/', views.agregar_producto, name="agregar"),
    
     #este manda el parametro 
    path('agregar/<str:producto_id>/', views.agregar_producto, name="agregar"),
    

    #quitar un producto con boton 
   
   #este checa si exsite
    path('restar/', views.restar_producto, name="restar"),
    #este manda el parametro 
    path('restar/<str:producto_id>/', views.restar_producto, name="restar"),


   

    

]

urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) +static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)






