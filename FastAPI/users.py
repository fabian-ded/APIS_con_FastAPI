#para iniciar el servidor en FastAPI : uvicorn users:app --reload

from fastapi import FastAPI
from pydantic import BaseModel #esta importacion sirve para crear etidades es decir crear clases orientadas a objetos 

app = FastAPI()


#Entidad users

class User(BaseModel):#aqui se crea una clase porque es mas facil definir las caracteristicas de los usuarios si fura una aplicacion de verdad
    name : str #se definen asi sin contructor ni nada eso es lo que hace el "BaseModel" solo debemos colocar como se llama la caracteristica y que tipo de dato debe contener
    surname : str
    url: str
    age : int
    
users_list=[User(name="Fabian", surname="Silva", url="https://fab.com", age=19), #aqui se define la lista que es donde tiene todos los datos de los usuarios, pero deberia der la base de datos, pero estamos haciendo ejeplos
            User(name="Snatiago", surname="Sobelo", url="https://san.com", age=21),
            User(name="Mabelyn", surname="Frentes", url="https://mab.com", age=18)]


@app.get("/usersjson")
async def usersjson(): #muy improtante es tener claro como se va a llamar cada funcion para no ser confundido
    return [{"name":"Fabian", "surname":"Silva", "url":"https://fab.com", "age":19},
            {"name":"Snatiago", "surname":"Sobelo", "url":"https://san.com", "age":21},#esta es uhna manera de hacerlo manual, que es muy largo por eso se crea la clase para que sea mas eficiente
            {"name":"Mabelyn", "surname":"Frentes", "url":"https://mab.com", "age":18}]
    
@app.get("/Users")#aqui se llama desde la url para que se muestren los datos de los usuarios
async def Users():
    return users_list #aqui se muestra la lista de los datos de los usuarios