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
from .models import DatosA, Profile, ModificacionDatos, Comentarios  # Importa el modelo de Profile
#https://www.clubdetecnologia.net/blog/2020/uso-del-pylint-para-analizar-codigo-en-python/ # este es del pylint que marcaba erorr las importacinoes 
from django.shortcuts import render
from django.template import RequestContext
from django import template  # Importa el módulo template de Django
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, loader
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import get_template
from django.template.loader import render_to_string
import smtplib
from django.shortcuts import render, redirect, get_object_or_404
from email.message import EmailMessage
from django.utils.html import strip_tags
from django.db.models import Sum, F, FloatField
from django.core.mail import send_mail

from django.core.paginator import Paginator
from django.views.defaults import page_not_found

import json

from .forms import UserRegisterForm, ComentarioForm
from django.utils.timezone import datetime, now
# Create your views here.
from .context_processor import importe_total_carro
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
  
  
""" 
#Este si funciona y los datos pe los pone arriba 
@login_required
def perfil(request):
    user = request.user
    try:
        datos = DatosA.objects.get(user=user)
    except DatosA.DoesNotExist:
        datos = None
    
    context = {'user': user, 'datos': datos}
    return render(request, 'social/perfil.html', context)

  """
  
#si no  quito  DatosA.all() los datos arribas no  aparecen 
@login_required
def perfil(request):
    user = request.user
    
    datos_exists = DatosA.objects.filter(user=user).exists()
   
   
    if not datos_exists:
    # Crea un nuevo objeto DatosA para el usuario
     DatosA.objects.create(user=user)
    
# Ahora puedes obtener el objeto DatosA sin preocuparte por el error
    datos = DatosA.objects.get(user=user)

    # Recupera todas las modificaciones relacionadas con los datos actuales del usuario

    modificaciones = ModificacionDatos.objects.filter(datos=datos).order_by('-timestamp_modificacion')

# Filtra las modificaciones para incluir solo las que realmente se han cambiado
    modificaciones_filtradas = []
    for modificacion in modificaciones:
        #if modificacion.telefono_anterior != datos.telefono or modificacion.direccion_anterior != datos.direccion:
          modificaciones_filtradas.append(modificacion)
          
    paginator = Paginator(modificaciones_filtradas, 5)
    pagina = request.GET.get("page") or 1
    modificaciones_filtradas= paginator.get_page(pagina)
    pagina_actual = int(pagina)
    paginas = range(1, modificaciones_filtradas.paginator.num_pages + 1)
    

    context = {'user': user, 'datos': datos, 'modificaciones': modificaciones_filtradas , 'modificaciones_filtradas': modificaciones_filtradas,  'paginas': paginas, 'pagina_actual': pagina_actual}
    return render(request, 'social/perfil.html', context)



@login_required
def comentarios(request):
	current_user = get_object_or_404(User, pk=request.user.pk)
	if request.method == 'POST':
		form = ComentarioForm(request.POST)
		if form.is_valid():
			comen = form.save(commit=False) #poara ver quien la esta enviando
			comen.user = current_user
			comen.save()
			messages.success(request, 'Comentario Publicado')
			return redirect('feed')
	else:
		form = ComentarioForm()
	return render(request, 'social/comentarios.html', {'form' : form })
  

""""
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


from django.utils import timezone


@login_required
def actualizar_perfil(request):
    user = request.user
    datos_actual, created = DatosA.objects.get_or_create(user=user)
    
    if request.method == 'POST':
        telefono = request.POST.get('telefono')
        direccion = request.POST.get('direccion')
        email = request.POST.get('email')
        username = request.POST.get('username')
        
        nueva_imagen = request.FILES.get('image', None)

        telefono_anterior = request.POST.get('telefono_anterior', '')
        direccion_anterior = request.POST.get('direccion_anterior', '')
        
        email_anterior = request.POST.get('email_anterior', '')
        username_anterior = request.POST.get('username_anterior', '')
        
        
        
        
        email_anterior = user.email  # Obtener el valor actualizado del correo electrónico
        username_anterior = user.username  # Obtener el valor actualizado del nombre de usuario
        imagen_anterior = user.profile.image if nueva_imagen else None

        # Crear un nuevo objeto ModificacionDatos para el historial
        modificacion = ModificacionDatos(
            datos=datos_actual,
            timestamp_modificacion=datetime.now(),
            telefono_anterior=telefono_anterior,
            direccion_anterior=direccion_anterior,
            imagen_anterior=imagen_anterior,
            username_anterior=username_anterior,
            email_anterior=email_anterior
        )

        cambios_realizados = False  # Variable para rastrear si se han realizado cambios

        # Verificar si hay cambios y actualizar el objeto ModificacionDatos en consecuencia
        if telefono_anterior != telefono:
            modificacion.telefono_nuevo = telefono
            cambios_realizados = True

        if direccion_anterior != direccion:
            modificacion.direccion_nueva = direccion
            cambios_realizados = True

        if username_anterior != username:
            modificacion.username_nuevo = username
            cambios_realizados = True

        if email_anterior != email:
            modificacion.email_nuevo = email
            cambios_realizados = True

        if nueva_imagen != imagen_anterior:
            modificacion.imagen_anterior = imagen_anterior
            modificacion.imagen_nueva = nueva_imagen
            cambios_realizados = True

        # Guardar la modificación solo si se han realizado cambios
        if cambios_realizados:
            modificacion.save()

        # Actualizar los datos en DatosA solo si se han realizado cambios
        if cambios_realizados:
            datos_actual.telefono = telefono
            datos_actual.direccion = direccion
            datos_actual.save()


    
        # Actualizar el correo electrónico y el nombre de usuario del usuario
        user.email = email
        user.username = username
        user.save()
        
        
        # Actualizar la imagen de perfil si se proporciona una nueva
        if nueva_imagen:
            user.profile.image = nueva_imagen
            user.profile.save()

        if username_anterior != user.username:
            messages.info(request, f'Cambio en el usuario: {username_anterior} ----> {user.username}')
        else: 
            messages.info(request, 'No hubo cambio de usuario')

        if email_anterior != user.email:
            messages.info(request, f'Cambio en el correo: {email_anterior} ----> {user.email}')
        else: 
            messages.info(request, 'No hubo cambio de correo')
            

        if nueva_imagen != imagen_anterior:
            messages.info(request, f'Cambio en la imagen: {imagen_anterior} ----> {nueva_imagen}')
        else: 
            messages.info(request, 'No hubo cambio en la imagen')
             
        if telefono != telefono_anterior:
            messages.info(request, f'Cambio en el telefono: {telefono_anterior} ----> {telefono}')
        else:
            messages.info(request, 'No hubo cambio de telefono')

        if direccion != direccion_anterior:
            messages.info(request, f'Cambio en la dirección: {direccion_anterior} ----> {direccion}')
        else: 
            messages.info(request, 'No hubo cambio de direccion')

        messages.success(request, 'Tu perfil ha sido actualizado correctamente.')
        return redirect('perfil')

    else:
        # Mostrar el formulario de actualización de perfil
        context = {'datos_actual': datos_actual, 'user': user}
        return render(request, 'social/actualizar_perfil.html', context)

      
    

def PagHis(request):

  return render(request, 'social/paginacion_historial.html')

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



@login_required # solo los usuairos autneticado pueden entrar 
def consultar_historial(request):
    
 # obtiene todos los usuarios y asignar a selected_user si se selecciona uno    
    users = User.objects.all() #aqui usuers accede a todos los elemtneos del modelo usuario
    selected_user = None #esta es la bandera para ver si ya se seleccion inicializarlo en NONE
#representar el usuario que ha sido seleccionado a través del menú desplegable en la interfaz de usuario.


# obtiene todas las modificaciones ordenadas por timestamp_modificacion de forma descendente
    historial = ModificacionDatos.objects.all().order_by('-timestamp_modificacion')
    campos = ModificacionDatos._meta.fields # este es para los campos del modelo 
    
# verifica si la solicitud es de tipo GET porque solo se va a obtener, no se va a aenviar nada 
    if request.method == 'GET':
           # Obtener el ID del usuario seleccionado desde los parámetros de la URL
     selected_user_id = request.GET.get('selected_user') #aqui jalo el id del usuario seleccionado
     
# Verifica si se ha seleccionado un usuario
    if selected_user_id:
        try:
   # Intentar obtener el usuario seleccionado
#pk es la primary key 
            selected_user = User.objects.get(pk=selected_user_id)
   # Filtrar el historial solo para el usuario seleccionado
   
#datos es el cmapo de mi modelo que tiene la llave foranea 
            historial = ModificacionDatos.objects.filter(datos__user=selected_user).order_by('-timestamp_modificacion')
        except User.DoesNotExist:   # Manejar la excepción si el usuario no existe
            selected_user = None
            historial = ModificacionDatos.objects.all().order_by('-timestamp_modificacion')
    else:
        selected_user = None
        historial = ModificacionDatos.objects.all().order_by('-timestamp_modificacion')

    context = {'historial': historial, 'users': users, 'selected_user': selected_user, 'campos': campos}
    return render(request, 'social/consultar_historial.html', context)




@login_required # solo los usuairos autneticado pueden entrar 
def consultar_posts(request):
    
 # obtiene todos los usuarios y asignar a selected_user si se selecciona uno    
    users = User.objects.all() #aqui usuers accede a todos los elemtneos del modelo usuario
    selected_user = None #esta es la bandera para ver si ya se seleccion inicializarlo en NONE
#representar el usuario que ha sido seleccionado a través del menú desplegable en la interfaz de usuario.


# obtiene todas las modificaciones ordenadas por timestamp_modificacion de forma descendente
    comentarios = Comentarios.objects.all().order_by('-timestamp')
    campos = Comentarios._meta.fields # este es para los campos del modelo 
    
# verifica si la solicitud es de tipo GET porque solo se va a obtener, no se va a aenviar nada 
    if request.method == 'GET':
           # Obtener el ID del usuario seleccionado desde los parámetros de la URL
     selected_user_id = request.GET.get('selected_user') #aqui jalo el id del usuario seleccionado
     
# Verifica si se ha seleccionado un usuario
    if selected_user_id:
        try:
   # Intentar obtener el usuario seleccionado
#pk es la primary key 
            selected_user = User.objects.get(pk=selected_user_id)
   # Filtrar el historial solo para el usuario seleccionado
   
#datos es el cmapo de mi modelo que tiene la llave foranea 
            comentarios = Comentarios.objects.filter(user=selected_user).order_by('-timestamp')
        except User.DoesNotExist:   # Manejar la excepción si el usuario no existe
            selected_user = None
            comentarios = Comentarios.objects.all().order_by('-timestamp')
    else:
        selected_user = None
        comentarios = Comentarios.objects.all().order_by('-timestamp')

    context = {'comentarios': comentarios, 'users': users, 'selected_user': selected_user, 'campos': campos}
    return render(request, 'social/consultar_posts.html', context)




@login_required # solo los usuairos autneticado pueden entrar 
def consultar_compras(request):
  
    # Simulación de datos, reemplázalos con tus propios datos de la base de datos
    labels = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo']
    valores = [12, 19, 7, 5, 2]

    # Convierte los datos a formato JSON
    data = {'labels': labels, 'valores': valores}
    datos_json = json.dumps(data)

    context = {'datos_json': datos_json}
    return render(request, 'social/consultar_compras.html', context)
  
  







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




