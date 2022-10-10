from django.urls import path
from . import views
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', views.feed, name ="feed"),
    url('^perfil/$' , views.perfil, name="perfil"),
    url('^register/$' , views.registro, name="registro"),
    url('^login/$' , LoginView.as_view(template_name='social/login.html'), name="login"),
    url('^logout/$' , LogoutView.as_view(template_name='social/logout.html'), name="logout"),
    url('^acceso/$' , views.retorno, name="pruebita"),
    url('^registro/$' , views.contactosregistro, name="contactosregistro"),
    url('^consulta/$' , views.consultar, name="consultas"),
    url('^carru/$' , views.carrusel, name="carrusel"),
    url('^correo/$' , views.mandarcorreo, name="mandarcorreo"),
    url('^consultarcorreo/$' , views.consultarc, name="consultarc"),
]




