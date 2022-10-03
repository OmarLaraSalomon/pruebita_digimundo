
from django.shortcuts import render, redirect
from .models import *
from .models import Post
from .forms import UserRegisterForm
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

#django nos permite tener forms#


# Create your views here.
# el context es para pedir datos a base 

def feed(request):
 
  return render(request, 'social/feed.html')


def perfil(request):
 
  return render(request, 'social/perfil.html')

 
def registro(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			messages.success(request, f'Usuario {username} creado')
			return redirect('feed')
	else:
		form = UserRegisterForm()

	context = { 'form' : form }
	return render(request, 'social/registro.html', context)



 


def login(request):
 
  return render(request, 'social/login.html')

@login_required
def retorno(request):
 
  return render(request, 'social/pruebita.html')

def contactosregistro(request):
  if request.method == 'POST':  
       
        datos = Post.objects.create(
          
                user_id=request.POST['user'], 
                first_name=request.POST['nombre'], 
                last_name=request.POST['apellidos'], 
                telefono=request.POST['telefono'], 
                telefono_casa=request.POST['telefono_casa'], 
                nacimiento=request.POST['nacimiento'], 
                direccion=request.POST['direccion'],  
                contacto_emergencia=request.POST['contacto_emergencia'], 
                telefono_emergencia=request.POST['telefono_emergencia'], 
                puesto=request.POST['puesto'],
                departamento=request.POST['departamento'],
                is_leader=request.POST['lider'],
            
          )
        datos.save()
  return render(request, 'social/contacto.html')



