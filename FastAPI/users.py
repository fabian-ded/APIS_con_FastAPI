#para iniciar el servidor en FastAPI : uvicorn users:app --reload

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel #esta importacion sirve para crear etidades es decir crear clases orientadas a objetos 

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


@app.get("/usersjson")
async def usersjson(): #muy improtante es tener claro como se va a llamar cada funcion para no ser confundido
    return [{"name":"Fabian", "surname":"Silva", "url":"https://fab.com", "age":19},
            {"name":"Santiago", "surname":"Sobelo", "url":"https://san.com", "age":21},#esta es uhna manera de hacerlo manual, que es muy largo por eso se crea la clase para que sea mas eficiente
            {"name":"Mabelyn", "surname":"Frentes", "url":"https://mab.com", "age":18}]
    
@app.get("/Users")#aqui se llama desde la url para que se muestren los datos de los usuarios
async def Users():
    return users_list #aqui se muestra la lista de los datos de los usuarios

#ejemplo mio, para llamar mediante el id "path"
@app.get("/ejemplo/{id}")
async def user(id:int):
    return users_list[id]

#ejemplo del curso para llamar mediante el id "path"
@app.get("/user/{id}")
async def user(id:int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"error":"no se ha encontrado el usuario"}

#ejemplo del curso query
@app.get("/userquery/")
async def user(id:int):
    return Buscar(id)#aqui se llama la funcion que se creo para que haga la logica de comprar los id con la url pasada
    
def Buscar(id: int): #esta es una manera practica para no tener todo en el mismo http y asi es una manera facil de hacerlo y con menos errores  
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]#ese "[0]" que se ve ahi significa que buscara el primer resultado de la busqueda que tenga parecido
    except:
        return {"error":"no se ha encontrado el usuario"}


#ejemplo mio
@app.get("/ejemploquery/")
async def user(id:int, name:str):
    users = filter(lambda user: user.id == id and user.name == name, users_list)
    try:
        return list(users)[0]
    except:
        return {"error":"no se ha encontrado el usuario"}
    
    