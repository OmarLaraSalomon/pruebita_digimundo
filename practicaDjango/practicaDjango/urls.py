"""practicaDjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , re_path ,include
from django.conf.urls import handler404
from django.conf.urls import handler404, handler500
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import handler404, handler500
from appDijango.views import pages

from appDijango import views
urlpatterns = [
    path("admin/", admin.site.urls),
    path('',include('appDijango.urls')),
    re_path(r'^.*\.*', views.pages, name='pages'),  # para rutar todas las URL que coinciden con cualquier patrón

]
##las vistas creadas
