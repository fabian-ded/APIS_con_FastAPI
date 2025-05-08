#Herramientas para documentacion de la aplicacion

#http://127.0.0.1:8000/docs
#http://127.0.0.1:8000/redoc

#importante siempre estar en esta direccion : PS C:\Users\admin\OneDrive\Desktop\Backenn\FastAPI
#para iniciar el servidor en FastAPI : uvicorn main:app --reload

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root(): #muy improtante es tener claro como se va a llamar cada funcion para no ser confundido
    return  "que mas bro"

@app.get("/url")
async def url():
    return {"url":"http://127.0.0.1:8000/docs"}