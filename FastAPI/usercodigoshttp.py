#podemos ir a la pagina de "http de mozilla" que es donde esta especificado cada codigo del http con su significado de respuesta y esto nos ayuda mucho

from fastapi import FastAPI, HTTPException #aqui se importan lo que es las funciondes de FastApi y ademas el exception para el manejo de errores
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


def Buscar(id: int): #esta es una manera practica para no tener todo en el mismo http y asi es una manera facil de hacerlo y con menos errores  
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"error":"no se ha encontrado el usuario"}

@app.post("/userquery/", status_code=201)#aqui se pasa que cada vez que se haga bien la operacion se mande un mensaje de tipo "201" que es un mensaje de codigo http para entender
async def user(user:User): #aqui se pasa el usuario a crear
    if type(Buscar(user.id)) == User: #aqui se busca si el usuario existe, si existe no se creara y se busca mediante el id
        raise HTTPException(status_code=404, detail="El usuraio ya existe") #aqui toca agregar el "raise" que es la funcion que nos permite mostrar el codigo y ademas toca utilizar el 
    #excepcion para manejo de errores y colocar que stado va estar el error y que mensaje saldra en pantalla.
    else:
        users_list.append(user)#y si no existe, se procede a crear el usuario nuevo en postman o thunderclient, abriendo la lista de los usuarios
    return user
