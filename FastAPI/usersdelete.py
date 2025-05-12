from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

#Entidad users

class User(BaseModel):#aqui se crea una clase porque es mas facil definir las caracteristicas de los usuarios si fura una aplicacion de verdad
    id : int
    name : str #se definen asi sin contructor ni nada eso es lo que hace el "BaseModel" solo debemos colocar como se llama la caracteristica y que tipo de dato debe contener
    surname : str
    url: str
    age : int
    
users_list=[User(id= 1, name="Fabian", surname="Silva", url="https://fab.com", age=19), #aqui se define la lista que es donde tiene todos los datos de los usuarios, pero deberia der la base de datos, pero estamos haciendo ejeplos
            User(id= 2, name="Santiago", surname="Sobelo", url="https://san.com", age=21),
            User(id= 3,name="Mabelyn", surname="Frentes", url="https://mab.com", age=18)]

@app.get("/users")#aqui se llama desde la url para que se muestren los datos de los usuarios
async def Users():
    return users_list #aqui se muestra la lista de los datos de los usuarios

#ejemplo del curso query
@app.get("/user/")
async def user(id:int):
    return Buscar(id)#aqui se llama la funcion que se creo para que haga la logica de comprar los id con la url pasada
    
def Buscar(id: int): #esta es una manera practica para no tener todo en el mismo http y asi es una manera facil de hacerlo y con menos errores  
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"error":"no se ha encontrado el usuario"}


@app.post("/userquery/")
async def user(user:User): #aqui se pasa el usuario a crear
    if type(Buscar(user.id)) == User: #aqui se busca si el usuario existe, si existe no se creara y se busca mediante el id
        return{"error": "El usuraio ya existe"}
    else:
        users_list.append(user)#y si no existe, se procede a crear el usuario nuevo en postman o thunderclient, abriendo la lista de los usuarios
    return user

@app.delete("/userdelete/{id}")
async def user(id:int):
    found = False #esto sirve para saber si ya se hizo la actualizacion es decir si se actualizo pasara a true como esta mas abajo del codigo
    for index, mirar_usuario in enumerate(users_list):#aqui se hace un bucle para buscar todos los usuarios en la lista de arriba
        #ademas se agrega un "index" y un "enumerate" para enuerar a cada usuario
        if mirar_usuario.id == id: #se compara de que el id del usuario enviado por la url como el de el json sea iguales
            del users_list[index] #se elimina el usuario
            found = True #aqui
        
    if not found:
        return {"error": "no se ha eliminado el usuario"}#si sale error "404"
    else:
        return {"message": f"Usuario con id {id} eliminado correctamente"} #Respuesta de éxito