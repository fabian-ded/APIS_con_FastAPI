from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from jose import jwt, JWTError #aqui se importa la libreria Para crear y manejar los tokens de autenticación.
from passlib.context import CryptContext# Para hashear y verificar contraseñas de forma segura, pero "passlib", Es fundamental para almacenar contraseñas de forma segura, ya que incluso si alguien accede a tu base de datos, no podrá ver las contraseñas originales.
#y "cryptcontext" es el predeterminado para nuevas contraseñas, y cómo manejar la verificación de contraseñas que podrían haber sido hasheadas con algoritmos más antiguos.
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm #la primera funcion importada nos permite jestionar la autenticacion del usuario y contraseña
#la segunda funcion realiza una capturacion de ese usuario y contraseña para que el backen sepa si el usuario hace parte de nuestro sistema

ALGORITHM = "HS256" # Define el algoritmo de firma para los JWT: HMAC con SHA256 y asi mismo usa la misma 'SECRET' para firmar y verificar que el token esta creado por el sistema.
ACCESS_TOKEN_DURATION = 1 #aqui estamos diciendo que el token va a durar activo 1 minuto
SECRET = "ba5c8337a2059869c7509e928e45e372236f5cee2b4c03aa0881fac8e9fe0453" #esto es una clave secreta que solo el sistema sabe y puede usarlo


router = APIRouter()

crypt = CryptContext(schemes=["bcrypt"])# Aquí le estamos diciendo que use el algoritmo bcrypt que es para las contraseñas encryptadas.
oauth2 = OAuth2PasswordBearer(tokenUrl="login")#aqui se realiza esta linea que es la encargada de manejar el sistema de autenticacion mediante el "TokenUrLl:login" que se va a pasar abajo cuando se haga la logica de ingresar la contrase y usuario

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
        "full_name": "fabian silva",
        "email" : "fab@gmail.com",
        "disabled" : False,
        "password": "$2a$12$ewpcjCV/zripM5HeyCaxQ.JFrq3sStdsLWzwhFyTWQ2j2y6ybPl.S"#aqui se coloca la contraseña encryptada
    },
    "santiago": {
        "username": "santiago",
        "full_name": "santiago sobelo",
        "email" : "san@gmail.com",
        "disabled" : True,
        "password": "$2a$12$vZNLrxCRkuAAIRRDnIx7ueoGSNbia01LRF9yM5x9wUIXhJnNFGu.e"
    }
}

def buscar_usuario_db(username: str):#aqui el usuario nos da su nombre
    if username in users_db: #se mira si si esta en la base de datos
        return Userdb(**users_db[username]) #retornara, si esta en la base de datos

def buscar_usuario(username: str):#aqui el usuario nos da su nombre
    if username in users_db: #se mira si si esta en la base de datos
        return User(**users_db[username]) #retornara los datos de este, si esta en la base de datos

async def auth_user(token: str = Depends(oauth2)): #aqui se verifica el token 
    Exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                              detail="Credenciales de autenticacion invalidas",
                              headers={"WWW-Authenticate": "Bearer"})
    try:
        username = jwt.decode(#este "jwt.decode" se utiliza para descodificar el token.
                            token, #Es el token que envia el cliente
                            SECRET, #Es la clave secreta que se usa para firmar/crear el token que Solo el servidor la conoce.
                            #Sirve para verificar que el token no haya sido alterado y que fue emitido por el mismo servidor.
                            algorithms=[ALGORITHM]#aqui se especifica el algoritmo de firma que se usó (en este caso, HS256)
                              ).get("sub")
        if username is None:
            raise Exception
        
    except JWTError:
        raise Exception
    
    return buscar_usuario(username)

async def current_user(user: User = Depends(auth_user)):#aqui se va a pasar el token a utilizar
    if user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Usuario inactivo")
    return user #si sale bien nos retornara la informacion del usuario autenticado


@router.post("/login/robusto") 
async def login(form: OAuth2PasswordRequestForm = Depends()):#aqui se atrapa la contraseña y usuario
    user_db = users_db.get(form.username)#aqui esta la logica par a buscar si coincide con lo que se tiene en la base de datos
    if not user_db:#sino existe arroja un error
        raise HTTPException(status_code=400, detail="El usuario no es correcto")

    user = buscar_usuario_db(form.username) #aqui ya se tiene tanto el nombre que nos paso el usuario como el nombre que se tiene en la base de datos
    if not crypt.verify(form.password, user.password):#aqui se compara de que sino es igual la contraseña que paso el usuarios a la que se tiene en la base de datos 
        raise HTTPException(status_code=400, detail="La contraseña no es correcta")#nos arroja un error
    
    access_token = {"sub": user.username, "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)}#aqui estamos dando la logica de cuanto tiempo tiene permiso el token para ser desactivado
    
    return{"access_token": jwt.encode(#este "jwt.encode" se utiliza para crear (codificar y firmar) un JWT.
                                    access_token,#aqui va la logica del permiso de access_token que es el tiempo
                                    SECRET,#aqui se usa para afirmar el token y verificar su autenticidad
                                    algorithm=ALGORITHM),#y aqui es el metodo para crear el token
           "token_type": "bearer"}#aqui si todo salio bien se le da permisos de autenticacion para que pueda utilizar la aplicacion y pueda buscar etc..

@router.get("/users/me/robusto")
async def yo(user: User = Depends(current_user)):#aqui permite que el usuario autenticado pueda buscar sus propios datos
    return user