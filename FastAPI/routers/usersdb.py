#para iniciar el servidor en FastAPI : uvicorn users:app --reload

from fastapi import APIRouter, HTTPException, status
from db.models.user import User #para importar la clase que se creo de "User" para la base de datos los datos que debe tener cada usuario
from db.cliente import db_client #se importa la base de datos
from db.schemas.user import user_schema # se importa

router = APIRouter(prefix="/userdb",
                   tags=["userdb"])#El "prefix" es una funcion que nos permite colocar la ruta establecida para todo el crud que se haga aqui

    
users_list=[()]


@router.get("/")#aqui se llama desde la url para que se muestren los datos de los usuarios
async def Users():
    return users_list #aqui se muestra la lista de los datos de los usuarios

#ejemplo mio, para llamar mediante el id "path"
@router.get("/{id}")
async def user(id:int):
    return users_list[id]

#ejemplo del curso para llamar mediante el id "path"
@router.get("/{id}")
async def user(id:int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        raise HTTPException(status_code=404, detail="no se ha encontrado el usuario")

#ejemplo del curso query
@router.get("/")    
async def user(id:int):
    return Buscar(id)#aqui se llama la funcion que se creo para que haga la logica de comprar los id con la url pasada
    
def Buscar(id: int): #esta es una manera practica para no tener todo en el mismo http y asi es una manera facil de hacerlo y con menos errores  
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]#ese "[0]" que se ve ahi significa que buscara el primer resultado de la busqueda que tenga parecido
    except:
        raise HTTPException(status_code=404, detail="no se ha encontrado el usuario")

#ejemplo mio
@router.get("/")
async def user(id:int, name:str):
    users = filter(lambda user: user.id == id and user.name == name, users_list)
    try:
        return list(users)[0]
    except:
        return {"error":"no se ha encontrado el usuario"}
    
@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def user(user: User): #aqui se pasa el usuario a crear
    #if type(Buscar(user.id)) == User: #aqui se busca si el usuario existe, si existe no se creara y se busca mediante el id
        #raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="el usuario ya existe")

    user_dict = dict(user)
    del user_dict["id"]

    id = db_client.local.users.insert_one(user_dict).inserted_id

    new_user = user_schema(db_client.local.users.find_one({"_id" : id}))

    return User(**new_user)



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