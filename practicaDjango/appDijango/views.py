
from multiprocessing import context
from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
from .models import Post
from .models import Correo
from .models import Productos
from .models import Servicios
from .carro import Carro
from .models import Pedido
from .models import LineaPedido
from .models import Noticias

from .forms import UserRegisterForm
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import get_template
from django.template.loader import render_to_string
import smtplib
from email.message import EmailMessage
from django.utils.html import strip_tags
from django.db.models import Sum, F, FloatField
from django.core.mail import send_mail
from decimal import Decimal  # Importa Decimal para manejar valores monetarios
#django nos permite tener forms#


from .context_processor import importe_total_carro
# Create your views here.

# el context es para pedir datos a base 

def layout(request):

  if request.user.is_authenticated:
        messages.success(request, "¡Bienvenido de nuevo!")
  else:
        messages.error(request, "Inicia sesión para acceder a todas las funciones.")
    
  
  return render(request, 'social/layout.html')



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


def consultar(request):
  info = Post.objects.all()
  
  context= {'posts': info}

  #correo = Correo.objects.all()
  
  #context= {'datos': correo}
  return render(request, 'social/consulta.html', context )





def carrusel(request):
 
  return render(request, 'social/carru.html')





def mandarcorreo(request):
  if request.method == 'POST':  
        correoPru=request.POST['correo_electronico']
        asunto= request.POST['nombre']+ ' '+ request.POST['apellidos']+ ', '+ request.POST['cargo']+ ' en '+ request.POST['empresa']+ ' con correo '+ request.POST['correo_electronico']+ ' \n ' +'Envio su informacion para una consulta con respecto al asunto: '+ request.POST['comentarios']+ ' \n '+ 'En breve sera contactado al numero ' + request.POST['telefono']
        datos = Correo.objects.create(
            nombre=request.POST['nombre'], 
            apellidos=request.POST['apellidos'], 
            correo_electronico=request.POST['correo_electronico'], 
            telefono=request.POST['telefono'],
            empresa=request.POST['empresa'],
            cargo=request.POST['cargo'],
            comentarios=request.POST['comentarios']
            )
        datos.save()
        
        send_mail(
    'Correo de Confirmacion',
    asunto,
    'Hola guapo',
    [correoPru,'weskermexx@gmail.com'],
    fail_silently=False
)
  context = {}
  return render(request, 'social/correo.html')
      


def consultarc(request):
  correo = Correo.objects.all()
  
  context= {'datos': correo}
  return render(request, 'social/consultarc.html', context )



def tiendita(request):

  return render(request, 'social/tienda.html')



def home(request):
 noticias=Noticias.objects.all()
  
 return render(request, 'social/home.html', {"noticias":noticias})




def servi(request):
  servicios=Servicios.objects.all()
  return render(request, 'social/servicios.html', {"servicios":servicios})



@login_required
def produ(request):

  productos=Productos.objects.all()

  if not request.user.is_authenticated:
        messages.warning(request, "Debes estar logueado para acceder a esta página.")
        return redirect('feed')  # Redirige a la página de inicio de sesión

  return render(request, 'social/productos.html', {"productos": productos})


def agregar_producto(request, producto_id=None):
    carro = Carro(request)
    producto = Productos.objects.get(id=producto_id)
    carro.agregar(producto=producto)
    return redirect("productos")



def eliminar_producto(request, producto_id=None):
    carro = Carro(request)
    producto = Productos.objects.get(id=producto_id)
    carro.eliminar(producto=producto)
    return redirect("productos")

def restar_producto(request, producto_id=None):
    carro = Carro(request)
    producto = Productos.objects.get(id=producto_id)
    carro.restar_producto(producto=producto)
    return redirect("productos")


def limpiar_carro(request):

    carro=Carro(request)

    carro.limpiar_carro()

    return redirect("productos")



def reiniciar(request):

    carro=Carro(request)

    carro.reiniciar()

    return redirect("home")



def procesar_pedido(request):
 
    pedido = Pedido.objects.create(user=request.user)  # damos de alta un pedido
    carro = Carro(request)  # cogemos el carro
    lineas_pedido = list()  # lista con los pedidos para recorrer los elementos del carro
    
    # Calcula el importe total del carrito
  

    for key, value in carro.carro.items():  # recorremos el carro con sus items
        producto = Productos.objects.get(id=key)
        cantidad = value['cantidad']
        precio_producto = producto.precio  # Obtén el precio del producto

        lineas_pedido.append(LineaPedido(
            producto=producto,
            cantidad=cantidad,
            user=request.user,
            pedido=pedido,
            precio=precio_producto # Asigna el precio del producto
       
        ))

    LineaPedido.objects.bulk_create(lineas_pedido)  # crea registros en BBDD en paquete
    total_pedido = importe_total_carro(request)  # Calcula el total del pedido antes de llamar a enviar_mail



    # Envía el correo electrónico y pasa el total como argumento
    enviar_mail(
        pedido=pedido,
        lineas_pedido=lineas_pedido,
        nombreusuario=request.user.username,
        email_usuario=request.user.email,
        total_pedido=total_pedido  # Pasa el total del pedido al contexto
      
    )

    reiniciar(request)

    # mensaje para el futuro
    messages.success(request, "El pedido se ha realizado correctamente")

    return redirect('productos')

    #return redirect('listado_productos')
    #return render(request, "tienda/tienda.html",{"productos":productos})
    

def enviar_mail(**kwargs):
    asunto="Gracias por el pedido"
       # Calcula el total del pedido aquí (supongamos que ya tienes el valor total_pedido)
    total_pedido = kwargs.get("total_pedido")
    mensaje=render_to_string("social/pedidos.html", {
        "pedido": kwargs.get("pedido"),
        "lineas_pedido": kwargs.get("lineas_pedido"),
        "nombreusuario":kwargs.get("nombreusuario"),
        "email_usuario":kwargs.get("email_usuario"),
        "total_pedido": kwargs.get("total_pedido")  # Agrega el total del pedido al contexto
                            
        })

    mensaje_texto=strip_tags(mensaje)
    from_email="weskermexx@gmail.com"
    to=kwargs.get("email_usuario")
    send_mail(asunto,mensaje_texto,from_email,[to], html_message=mensaje)




