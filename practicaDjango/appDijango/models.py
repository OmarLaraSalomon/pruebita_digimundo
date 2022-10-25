from distutils.command.upload import upload
from tabnanny import verbose
from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from importlib.resources import contents
from sqlite3 import Timestamp
from time import time, timezone

# Create your models here.
class Post (models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, null=True)
    first_name = models.CharField(max_length=250, null=True)
    last_name = models.CharField(max_length=250, null=True)
    telefono = models.CharField(max_length=250, null=True, unique=False)
    telefono_casa = models.CharField(max_length=250, null=True,  unique=False)
    nacimiento = models.CharField(max_length=250, null=True)
    direccion = models.CharField(max_length=300, null=True)
    contacto_emergencia = models.CharField(max_length=250, null=True)
    telefono_emergencia = models.CharField(max_length=250, null=True)
    puesto = models.CharField(max_length=250, null=True)
    departamento = models.CharField(max_length=250, null=True)
    is_leader = models.BooleanField(default=False,null=True)


class Correo (models.Model):
    nombre = models.CharField(max_length=90)
    apellidos = models.CharField(max_length=30)
    correo_electronico = models. EmailField(max_length=254)
    telefono = models.CharField(max_length=100)
    empresa = models.CharField(max_length=30)
    cargo = models.CharField(max_length=30)
    comentarios = models.TextField()



class CategoriaProd(models.Model):
    
    nombre = models.CharField(max_length=90)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name= "categoriaProd"
        verbose_name_plural= "categoriasProd"

  #salida 
    def __str__(self):
        return self.nombre




class Productos (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='productos', null=True)
    nombre = models.CharField(max_length=90)
    categoria = models.ForeignKey(CategoriaProd,on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to="productos", null=True, blank=True)
    precio= models.FloatField()
    disponibilidad=models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now_add=True)


    class Meta:
       
        verbose_name= "Producto"



class Servicios  (models.Model):
    
    titulo = models.CharField(max_length=90)
    contenido = models.CharField(max_length=90)
    imagen = models.ImageField(upload_to="servicios", null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now_add=True)


    class Meta:
       
        verbose_name= "servicio"
        verbose_name_plural= "servicios"
    
    
  #salida 
    def __str__(self):
        return self.titulo