class Carro:
    #iguallar la sesion del usuario con ese carro
    def __init__(self, request):
        self.request = request
        self.session = request.session
        carro = self.session.get("carro")
#EL CARRO DEBE DE ESTAR EN 0 PARA QUE COMIENCE A AGREGAR LOS PRODUCTOS, DESPUES DE AGREGAR YA PERMITE SUMAR

        if carro==0:
#si no hay carro 
#YA TIENE QUE HABER UN PRODUCTO PARA QUE SE CREE 
            carro=self.session["carro"] = {}
           #lo creamos 
        else:
            self.carro = carro
 #si ya esta y se sale el carro sigue ahi , el carro es el mismo que ya tenia antes de salir



#diccionario clave valor 
    def agregar(self, producto):
        if(str(producto.id) not in self.carro.keys()):
       #si el id del producto no esta en las claves del carro agregalo  kas key son las claves
            self.carro[producto.id]={

                "producto_id": producto.id,
                "nombre": producto.nombre,
                "precio": str(producto.precio),
                "cantidad": 1,
                "imagen": producto.imagen.url
            }


        else:
            for key, value in self.carro.items():
                #recorrer para cada clave valor en nuestro carro 
                if key==str(producto.id):
                    value["cantidad"]=value["cantidad"]+1
                    value["precio"]=float(value["precio"])+producto.precio
                    break
        self.guardar_carro()




    def guardar_carro(self):
        self.session["carro"] = self.carro
        self.session.modified = True





    def eliminar(self, producto):
        producto.id=str(producto.id)
       
        if producto.id in self.carro:
            del self.carro[producto.id]
            self.guardar_carro()




    def restar_producto(self, producto):
        for key, value in self.carro.items():
                if key==str(producto.id):
                    value["cantidad"]=value["cantidad"]-1
                    value["precio"]=float(value["precio"])-producto.precio
                    if value["cantidad"]<1:
                         self.eliminar(producto)
                    break
                        
        self.guardar_carro()



    def limpiar_carro(self):
        self.session["carro"] = {}
        self.session.modified = True 