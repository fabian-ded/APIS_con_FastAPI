#para iniciar el servidor en FastAPI : uvicorn users:app --reload

from fastapi import APIRouter, HTTPException, status
from db.models.user import User #para importar la clase que se creo de "User" para la base de datos los datos que debe tener cada usuario
from db.cliente import db_client #se importa la base de datos
from db.schemas.user import user_schema, users_schema # se importa el archivo que nos va extraer los datos que venga de la base de datos de mongoDB
from bson import ObjectId

router = APIRouter(prefix="/userdb",
                   tags=["userdb"])#El "prefix" es una funcion que nos permite colocar la ruta establecida para todo el crud que se haga aqui

    
users_list=[()]


@router.get("/", response_model=list[User])#aqui se llama desde la url para que se muestren los datos de los usuarios
async def users():
    #aqui se muestra la lista de los datos de los usuarios
    return users_schema(db_client.local.users.find())#con el find() estamos pidiendo toda la informacion que tengamos en la base de datos

#ejemplo mio, para llamar mediante el id "path"
@router.get("/{id}")
async def user(id:str):
    return Buscar("_id", ObjectId(id))

#ejemplo del curso query
@router.get("/")    
async def user(id:str):
    return Buscar("_id", ObjectId(id))#aqui se llama la funcion que se creo para que haga la logica de comprar los id con la url pasada

#ejemplo mio
@router.get("/")
async def user(id:int, name:str):
    users = filter(lambda user: user.id == id and user.name == name, users_list)
    try:
        return list(users)[0]
    except:
        return {"error":"no se ha encontrado el usuario"}



#ejemplo en la clase
#def Buscar_email(email: str): #esta es una manera practica para no tener todo en el mismo http y asi es una manera facil de hacerlo y con menos errores  
    #try:
    #    user = db_client.local.users.find_one({"email": email})#aqui buscamos el email que ingreso el usuario y el mail que tenemos en la base de datos
    #    if user is not None:#si user no esta es decir esta bacio se retorna lo de abajo
    #        return User(**user_schema(user))#aqui se retorna la informacion desempaquetada es decir un json limpio
    #except:
        #raise HTTPException(status_code=404, detail="no se ha encontrado el usuario")

# @router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
# async def user(user: User): #aqui se pasa el usuario a crear
#     if type(Buscar(user.email)) == User: #aqui se busca si el email existe, si existe no se creara y lanza un error
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST, detail="el usuario ya existe")

#     user_dict = dict(user)#aqui dict(user) convierte el objeto en un diccionario (porque Mongo no guarda objetos Pydantic).
#     del user_dict["id"]#aqui borramos "id" porque cuando se crea un usuario nuevo, Mongo genera su propio _id automáticamente.

#     id = db_client.local.users.insert_one(user_dict).inserted_id #aqui Se guarda el usuario en la base de datos y con inserted_id devuelve el ID (ObjectId) que Mongo le puso.
# #insert_one es para crear
#     new_user = user_schema(db_client.local.users.find_one({"_id" : id}))#aqui se esta recuperando la informacion del usuario mediante el "_id" y el "id", que anteriormente mongoDB ya nos habia
#     #dado su "_id" creado por el y se paso a la variable de "id" por eso se hace la comparacion
# #find_one es para comparar
#     return User(**new_user)#las dos "**" se utilizan para desempaquetar los archivos json y los transforma a argumentos de (id="4")




@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def user(user: User): #aqui se pasa el usuario a crear
    if type(Buscar("email",user.email)) == User: #aqui se busca si el email existe, si existe no se creara y lanza un error, "email" es field y "user.email" es key, en la funcion de buscar 
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="el usuario ya existe")

    user_dict = dict(user)#aqui dict(user) convierte el objeto en un diccionario (porque Mongo no guarda objetos Pydantic).
    del user_dict["id"]#aqui borramos "id" porque cuando se crea un usuario nuevo, Mongo genera su propio _id automáticamente.

    id = db_client.local.users.insert_one(user_dict).inserted_id #aqui Se guarda el usuario en la base de datos y con inserted_id devuelve el ID (ObjectId) que Mongo le puso.
#insert_one es para crear
    new_user = user_schema(db_client.local.users.find_one({"_id" : id}))#aqui se esta recuperando la informacion del usuario mediante el "_id" y el "id", que anteriormente mongoDB ya nos habia
    #dado su "_id" creado por el y se paso a la variable de "id" por eso se hace la comparacion
#find_one es para comparar
    return User(**new_user)#las dos "**" se utilizan para desempaquetar los archivos json y los transforma a argumentos de (id="4")



@router.put("/")
async def user(user: User):#aqui se pasa el usuario a buscar, que venga de la instancia de la clase User.
        found = False #esto sirve para saber si ya se hizo la actualizacion es decir si se actualizo pasara a true como esta mas abajo del codigo
        for index, mirar_usuario in enumerate(users_list):#aqui se hace un bucle para buscar todos los usuarios en la lista de arriba
            #ademas se agrega un "index" y un "enumerate" para enuerar a cada usuario
            if mirar_usuario.id == user.id: #se compara de que el id del usuario enviado por la url como el de el json sea iguales
                users_list[index] = user #se actualiza el nuevo usuario
                found = True #aqui
                break #frena el bucle
        if not found:
            raise HTTPException (status_code=status.HTTP_404_NOT_FOUND, detail="no se ha encontrado el usuario")
        else:
            return user #aqui es para ver que cambios hicimos es decir si salio todo bien con un "200"

@router.delete("/{id}")
async def user(id:int):
    found = False #esto sirve para saber si ya se hizo la actualizacion es decir si se actualizo pasara a true como esta mas abajo del codigo
    for index, mirar_usuario in enumerate(users_list):#aqui se hace un bucle para buscar todos los usuarios en la lista de arriba
        #ademas se agrega un "index" y un "enumerate" para enumerar a cada usuario
        if mirar_usuario.id == id: #se compara de que el id del usuario enviado por la url como el de el json sea iguales
            del users_list[index] #se elimina el usuario
            found = True #aqui
        
    if not found:
        raise HTTPException (status_code=status.HTTP_401_UNAUTHORIZED, detail="no se ha encontrado el usuario")
    else:
        return {"message": f"Usuario con id {id} eliminado correctamente"} #Respuesta de éxito
    
def Buscar(field: str, key): #field lo que se quiere buscar, key donde se quiere encontrar o buscar
    try:
        user = db_client.local.users.find_one({field: key})#aqui estamos haciendo es que "field" es el criterio de busqueda y "key" es la clave por la cual quiero buscar
        #es decir que si quiero buscar el nombre"field" en la base de datos, pues se pasa que en donde quieres que busque "key" ejemplo "nombre(field)==nombre(key)"  
        if user is not None:#si user no esta es decir esta bacio se retorna lo de abajo
            return User(**user_schema(user))#aqui se retorna la informacion desempaquetada es decir un json limpio
    except:
        raise HTTPException(status_code=404, detail="no se ha encontrado el usuario")