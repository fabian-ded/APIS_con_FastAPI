from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm #la primera funcion importada nos permite jestionar la autenticacion del usuario y contraseña
#la segunda funcion realiza una capturacion de ese usuario y contraseña para que el backen sepa si el usuario hace parte de nuestro sistema

app = FastAPI()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")#aqui se realiza esta linea que es la encargada de manejar el sistema de autenticacion mediante el "TokenUrLl:login" que se va a pasar abajo cuando se haga la logica de ingresar la contrase y usuario

#Entidad users

class User(BaseModel):#aqui se crea una clase porque es mas facil definir las caracteristicas de los usuarios si fura una aplicacion de verdad
    username: str
    full_name : str #se definen asi sin contructor ni nada eso es lo que hace el "BaseModel" solo debemos colocar como se llama la caracteristica y que tipo de dato debe contener
    email : str
    disabled : bool
    
class Userdb(User):
    password : str

users_db = {
    "fabian": {
        "username": "fabian",
        "full_name": "favian silva",
        "email" : "fab@gmail.com",
        "disabled" : False,
        "password": "123456"
    },
    "santiago": {
        "username": "santiago",
        "full_name": "santiago sobelo",
        "email" : "san@gmail.com",
        "disabled" : True,
        "password": "123"
    }
}
def buscar_usuario_db(username: str):#aqui el usuario nos da su nombre
    if username in users_db: #se mira si si esta en la base de datos
        return Userdb(**users_db[username]) #retornara, si esta en la base de datos

def buscar_usuario(username: str):#aqui el usuario nos da su nombre
    if username in users_db: #se mira si si esta en la base de datos
        return User(**users_db[username]) #retornara los datos de este, si esta en la base de datos

async def current_user(token: str = Depends(oauth2)):#aqui se va a pasar el token a utilizar
    user = buscar_usuario(token)#aqui la variable tendra el token optenido
    if not user:#sino esta en token manda un mensage de error
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales de autenticacion invalidas", headers={"WWW-Authenticate": "Bearer"})
    if user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario inactivo")
    return user #si sale bien nos retornara la informacion del usuario autenticado
    
@app.post("/login") 
async def login(form: OAuth2PasswordRequestForm = Depends()):#aqui se atrapa la contraseña y usuario
    user_db = users_db.get(form.username)#aqui esta la logica par a buscar si coincide con lo que se tiene en la base de datos
    if not user_db:#sino existe arroja un error
        raise HTTPException(status_code=400, detail="El usuario no es correcto")

    user = buscar_usuario_db(form.username) #aqui ya se tiene tanto el nombre que nos paso el usuario como el nombre que se tiene en la base de datos
    if not form.password == user.password:#aqui se compara de que sino es igual la contraseña que paso el usuarios a la que se tiene en la base de datos 
        raise HTTPException(status_code=400, detail="La contraseña no es correcta")#nos arroja un error
    
    return{"access_token": user.username, "token_type": "bearer"}#aqui si todo salio bien se le da permisos de autenticacion para que pueda utilizar la aplicacion y pueda buscar etc..

@app.get("/users/me")
async def yo(user: User = Depends(current_user)):#aqui permite que el usuario autenticado pueda buscar sus propios datos
    return user