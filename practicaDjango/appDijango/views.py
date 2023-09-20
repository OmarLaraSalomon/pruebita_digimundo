from django.conf import settings
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
from .models import Comentarios
from .models import DatosA, Profile  # Importa el modelo de Profile
#https://www.clubdetecnologia.net/blog/2020/uso-del-pylint-para-analizar-codigo-en-python/ # este es del pylint que marcaba erorr las importacinoes 
from django.shortcuts import render
from django.template import RequestContext
from django import template  # Importa el módulo template de Django
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, loader
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
from django.core.paginator import Paginator
from django.views.defaults import page_not_found
from django.template import RequestContext
from django.db.models import Q

# Create your views here.

# el context es para pedir datos a base 

def layout(request):

  if request.user.is_authenticated:
        messages.success(request, "¡Bienvenido de nuevo!")
  else:
        messages.error(request, "Inicia sesión para acceder a todas las funciones.")
    
  
  return render(request, 'social/layout.html')


"""
 #solo entrna los qyue estan autenticados
@login_required
def feed(request): #para porcesar las soliocitudes
    user = request.user  #user obtiene el objeto usuario actualemnte autenticado 
    infos = DatosA.objects.all() #infos obtiene todos los objetos de mi modelo 

    # Obtener los comentarios relacionados con cada usuario en la lista de Infos
    for info in infos:# itera un objeto y lo vuelve en info 
        info.comentarios = Comentarios.objects.filter(user=info.user) #para cada objeto info realiza una consulta en el modelo comentarios
#se filtran todos los comentarios que pertenecen al mismo usuario que el objeto info.usery se almacena con comentraios
    context = {'infos': infos} #se crea el diccionario 
    return render(request, 'social/feed.html', context)
"""


@login_required
def feed(request):
    user = request.user
    infos = DatosA.objects.all()

    context = {'infos': infos}
    return render(request, 'social/feed.html', context)
  
  

def perfil(request):
    user = request.user
    try:
        datos = DatosA.objects.get(user=user)
    except DatosA.DoesNotExist:
        datos = None
    
    context = {'user': user, 'datos': datos}
    return render(request, 'social/perfil.html', context)


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


from django.contrib.auth.models import User  # Importa el modelo de usuario de Django

def actualizar_perfil(request):
    if request.method == 'POST': #es de tipo POST, parar extraer los datos enviados del objeto rquiest en el formulario

        user = request.user # Procesar el formulario enviado por el usuario
        telefono = request.POST['telefono']
        direccion = request.POST['direccion'] #estos son los nuevos campos que va a tener el usuario
        email = request.POST['email']  # Nuevo correo electrónico
        username = request.POST['username']  # Nuevo nombre de usuario
        image = request.FILES.get('image')  # Obtiene la imagen de perfil cargada por el usuario
        
  #extrae varios campos del formulario que el usuario envió en la solicitud POST. 
        # Actualizar los datos en la base de datos
        
        #se crea objeto daotsA que es mi modelo asociado al usuario actual
#datos es mi objeto  # created  es una bandera booleana que indica si se creó un nuevo objeto 
#DaotsA si no existe created es true, si existe el objteo es false
        datos, created = DatosA.objects.get_or_create(user=user)  #get_or_create busca el objeto en la base de datos y lo crea si no existe
        datos.telefono = telefono
        datos.direccion = direccion
        datos.save() #guarda los nuesvos tregistos del  modelo 

#la vairbale datos almacena al objeto Datos

        # Actualizar el correo electrónico y el nombre de usuario del usuario
        user.email = email
        user.username = username

#Si el usuario ha cargado una nueva imagen de perfil  
# la vista busca o crea un objeto Profile asociado al usuario y actualiza la imagen de perfil en ese objeto.
        # Actualizar la imagen de perfil si se cargó una nueva
        
        if image: #checa si la imagen no es none significa que el usuario ha subido una nueva 
          
          #porfile es la vairable  que alamcena al objeto Profile       
            profile, created = Profile.objects.get_or_create(user=user) #ntentará obtener el perfil del usuario, y si no existe, lo creará automáticamente.
            profile.image = image #se obtinee el objeto profile se le asigna la nueva miagen a la propiedad image
            profile.save() #guarda los cambios en el objeto Profile

        user.save()  #guarda el usuario en la base de datos con los cambios realizados en su perfil.
        messages.success(request, 'Tu perfil ha sido actualizado correctamente.')
        return redirect('social/perfil.html')  # Cambia 'perfil' al nombre de tu vista de perfil
      
#no se ha enviado el formulario  pero si ha accedido el usuario a la vista 
#mostrar el formulario cyando accese sin enviar datos y ya luego se prellena
    else:
        # Mostrar el formulario de actualización de perfil
        datos, created = DatosA.objects.get_or_create(user=request.user) #obtener el objeto DatosA on el usuario actual
        context = {'datos': datos, 'user': request.user}
        return render(request, 'social/actualizar_perfil.html', context)
#el context  contiene los datos del usuario y su perfil,

def carrusel(request):
 
 
  return render(request, 'social/carru.html')

@login_required # se requiere loguear para acceder 
def pages(request): #la funcuion con la solicitud en parametroe 
    context = {} #un diccionario vacio para pasar lols datos de la plantilla
  
    try: # un try catch
        load_template = request.path.split('/')[-1]
#divide la URL de la solicitud en partes utilizando "/" como separador y toma la última parte, que debería ser el nombre del archivo HTML que se quiere cargar.
        if load_template == 'admin': #Comprueba si la última parte de la URL es "admin".
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = template.loader.get_template('social/' + load_template)#carga la platilla con la ruta 
#renderiza la plantilla con el concontexto  y retorna la repsuesta con la plantilla que se quiere 
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist: # esta es una excepcion  si se porduce una excepcion
        html_template = template.loader.get_template('social/error404.html')  # Usar template.loader
        return HttpResponse(html_template.render(context, request))
#si no se encuentra la url se carga una plantilla de error 404.
    except:
        html_template = template.loader.get_template('social/error500.html')  # Usar template.loader
        return HttpResponse(html_template.render(context, request))
      #si no se encuentra la url se carga una plantilla de error 404.
      
      
      
      
#404: página no encontrada
#def  pag_404_not_found(request, exception=None, template_name="social/error404.html"):
 #   response = render(request, template_name, status=404)
  #  return response
 
#500: error en el servidor
#def pag_500_error_server(request, exception=None, template_name="social/error500.html"):
 #   response = render(request, template_name)
  #  response.status_code = 500
   # return response


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
    'Correo de Contacto recibido, Esperando confirmación ',
    asunto,
    correoPru,
    ['weskermexx@gmail.com'],
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


def paginacion(request):

  return render(request, 'social/paginacion.html')

@login_required
def produ(request):

  productos=Productos.objects.all()
  paginacion= Paginator(productos, 3) #me va a paginar de 3 en 3 los porductos
  pagina= request.GET.get("page") or 1 #vamos a recuperar la pagina y vamos a obtener la page que va a venir en la url y si no existe nos va a mostrar 1, si no hay variable pagina nos quedamos con 1
  productos=paginacion.get_page(pagina) #los productos que necesitamos  son los articulos que necesitamos y retornamos para recuperarlos
  pagina_actual= int(pagina) #cuando venga por la url debe de ser stinrg y luego entero para cambiar la paginacion en la url dira pagina 1 o 2 
  paginas= range(1, productos.paginator.num_pages+1) #range ofrece varias frimas, permite definir el inico y final, le final se excluye, hace iteraciones el ultimo se excluye, 
  if not request.user.is_authenticated:
        messages.warning(request, "Debes estar logueado para acceder a esta página.")
        return redirect('feed')  # Redirige a la página de inicio de sesión

  return render(request, 'social/productos.html', {"productos": productos, "paginas":paginas, "pagina_actual": pagina_actual})


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




