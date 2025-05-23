from pydantic import BaseModel #esta importacion sirve para crear etidades es decir crear clases orientadas a objetos 

class User(BaseModel):#aqui se crea una clase porque es mas facil definir las caracteristicas de los usuarios si fura una aplicacion de verdad
    id : str | None = None #este "None" es porque MongoDB puede automaticamente agregarle un "id" sin que le pueda llegar cuando se haga un post, es decir que no se agrego un "id" en el post para
    #agergar los datos al mongoDB
    username : str #se definen asi sin contructor ni nada eso es lo que hace el "BaseModel" solo debemos colocar como se llama la caracteristica y que tipo de dato debe contener
    email: str