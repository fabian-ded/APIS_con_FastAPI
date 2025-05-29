#para iniciar el servidor en FastAPI : uvicorn users:app --reload

from fastapi import APIRouter, HTTPException, status
from db.models.user import User #para importar la clase que se creo de "User" para la base de datos los datos que debe tener cada usuario
from db.cliente import db_client #se importa la base de datos
from db.schemas.user import user_schema, users_schema # se importa el archivo que nos va extraer los datos que venga de la base de datos de mongoDB
from bson import ObjectId #importa ObjectId para poder trabajar con los identificadores únicos (_id) que MongoDB asigna automáticamente a cada dato (registro).

router = APIRouter(prefix="/userdb",
                   tags=["userdb"])#El "prefix" es una funcion que nos permite colocar la ruta establecida para todo el crud que se haga aqui

    


@router.get("/", response_model=list[User])#aqui se llama desde la url para que se muestren los datos de los usuarios, ademas el
#response_model=list[User] especifica que la respuesta HTTP será una lista de objetos JSON, es decir que lo que devuelva la funcion
#debe ser una lista de usuariossegun el modelo de "User"
async def users():
    #aqui se muestra la lista de los datos de los usuarios
    return users_schema(db_client.users.find())#con el find() estamos pidiendo toda la informacion que tengamos en la base de datos

#ejemplo mio, para llamar mediante el id "path"
@router.get("/{id}")
async def user(id:str):
    usuario = Buscar("_id", ObjectId(id))#aqui estamos diciendo que en la base de datos, busque el id que nos dio el usuario y como el id lo genero mongoDB usamos la libreria de 
#"ObjectId" que es el que trabaja con eses identificadores unicos de "_id".
    if usuario is not None:
        return usuario
    else:
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND, detail="no se ha encontrado el usuario")


#ejemplo mio
# @router.get("/")
# async def user(id:int, name:str):
#     users = filter(lambda user: user.id == id and user.name == name, users_list)
#     try:
#         return list(users)[0]
#     except:
#         return {"error":"no se ha encontrado el usuario"}



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




@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)#aqui estamos diciendo que debe de devolver al usuario un json segun la clase que tenemos deficida de User
async def user(user: User): #aqui se pasa el usuario a crear
    if type(Buscar("email",user.email)) == User: #aqui se busca si el email existe, si existe no se creara y lanza un error, "email" es field=base de datos y "user.email" es key=datos enviados por el usuario, en la funcion de buscar 
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="el usuario ya existe")

    user_dict = dict(user)#aqui dict(user) convierte el objeto en un diccionario (porque Mongo no guarda objetos Pydantic).
    del user_dict["id"]#aqui borramos "id" porque cuando se crea un usuario nuevo, Mongo genera su propio _id automáticamente.

    id = db_client.users.insert_one(user_dict).inserted_id #aqui Se guarda el usuario en la base de datos y con inserted_id devuelve el ID (ObjectId) que Mongo le puso.
#insert_one es para crear
    new_user = user_schema(db_client.users.find_one({"_id" : id}))#aqui se esta recuperando la informacion del usuario mediante el "_id" y el "id", que anteriormente mongoDB ya nos habia
    #dado su "_id" creado por el y se paso a la variable de "id" por eso se hace la comparacion
#find_one es para comparar
    return User(**new_user)#las dos "**" se utilizan para desempaquetar los archivos json y los transforma a argumentos de (id="4")



@router.put("/", response_model=User, status_code=status.HTTP_202_ACCEPTED)#aqui estamos diciendo que debe de devolver al usuario un json segun la clase que tenemos deficida de User
async def user(user: User):#aqui se pasa el usuario a buscar, que venga de la instancia de la clase User.
        
        user_dict = dict(user)#aqui dict(user) convierte el objeto en un diccionario (porque Mongo no guarda objetos Pydantic).
        del user_dict["id"]#aqui borramos "id" porque cuando se crea un usuario nuevo, Mongo genera su propio _id automáticamente.

        try:#manejo de error
            db_client.users.find_one_and_replace(
            {"_id": ObjectId(user.id)}, # 1. El filtro para encontrar el usuario
            user_dict ) # 2. El documento de reemplazo
            #es decir, cuando se incuentra el usuario ahora el "user_dict" pasa a tener los nuevos datos actualizados, haciendo que 
            #ahora los nuevos datos que tiene esta variable, remplace el contenido de los datos del usuario que tenia en ese momento
        except:
            return {"error": "no se ha actualizado el usuario"}
           
        return Buscar("_id", ObjectId(user.id)) #aqui es para ver que cambios hicimos es decir si salio todo bien con un "200"
    #ademas buscamos el usuario actualizado y lo mostramos al usuario


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def user(id: str):
    found = db_client.users.find_one_and_delete({"_id": ObjectId(id)})#aqui buscamos el usuarui y ademas "find_one_and_delete"
    #nos permite eliminar ese usuario
    if not found:
        raise {"error": "no se elimino el usuario"}
    
def Buscar(field: str, key): #field lo que se quiere buscar, key donde se quiere encontrar o buscar
    try:
        user = db_client.users.find_one({field: key})#aqui estamos haciendo es que "field" es el criterio de busqueda osea donde se tiene que buscar en la base de datos y "key" es la clave por la que el usuario esta buscando
        #es decir que si quiero buscar el nombre"key" en la base de datos, pues se pasa que en donde quieres que busque "field" donde esta ubicada esa imformacion en la base de datos ejemplo "nombre(field=base de datos)==nombre(key=dato enviado por el usuario)"  
        if user is not None:#si user no esta es decir esta bacio se retorna lo de abajo
            return User(**user_schema(user))#aqui se retorna la informacion desempaquetada es decir un json limpio
    except:
        raise HTTPException(status_code=404, detail="no se ha encontrado el usuario")