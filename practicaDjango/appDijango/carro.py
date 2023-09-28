
class Carro:
 #iguallar la sesion del usuario con ese carro
    def __init__(self, request): #constructor de la clase Carro  recibe el request 
        self.request=request #el self es porque es una vista basada en clase el self.request es para que este disponibvle toda la instancia de la clase
        self.session=request.session # se obtiene la sesion del usuario del objeto requiest y lo almacena en un atributo llamado self.session 
        carro=self.session.get("carro") # carro es un valor asociado que se van a usar
# esto es busca su ta existe un carrito de compras  

 #si no hay carro 
#YA TIENE QUE HABER UN PRODUCTO PARA QUE SE CREE        
        if not carro:
            carro=self.session["carro"]={}
       
        self.carro=carro #el carrito ya sea creado o recuperado se almacena en self.carro 

    def agregar(self,producto):
        if(str(producto.id) not in self.carro.keys()):
            self.carro[producto.id]={
                "producto_id":producto.id,
                "nombre":producto.nombre,
                "precio":str(producto.precio),
                "cantidad":1,
                "imagen":producto.imagen.url
            }
        else:
            for key, value in self.carro.items():
                if key==str(producto.id):
                    value["cantidad"]=value["cantidad"]+1
                    value["precio"]=float(value["precio"])+producto.precio
                    break
        self.guardar_carro()

    def guardar_carro(self):
        self.session["carro"]=self.carro
        self.session.modified=True

    def eliminar(self,producto):
        producto.id=str(producto.id)
        if producto.id in self.carro:
            del self.carro[producto.id]
            self.guardar_carro()

    def restar_producto(self, producto):
        for key, value in self.carro.items():
                if key==str(producto.id):
                    value["precio"]=float(value["precio"])-producto.precio
                    value["cantidad"]=value["cantidad"]-1
                    if value["cantidad"]<1:
                        self.eliminar(producto)
                    break
        self.guardar_carro()


    def limpiar_carro(self):
        self.session["carro"]={}
        self.session.modified=True


    def reiniciar(self):

        carro=self.session["carro"]={}
        self.carro=carro
        #carro =[]
        #self.carro=[]
        #self.carro["carro"] =[]
        #self.carro["carro"]= {}
        #request.carro["carro"]= []
      

   