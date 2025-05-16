from fastapi import APIRouter

router = APIRouter(prefix="/productos", tags=["productos"])#El "prefix" es una funcion que nos permite colocar la ruta establecida para todo el crud que se haga aqui

list_productos = ["Producto 1", "Producto 2", "Producto 3"]

@router.get("/")#aqui se puede ver que no esta la ruta, sino que esta ya re establecida arriba, dopnde la variable"router"
#usando ademas "routers" para ser llamado asi este corriendo el server en main
async def Productos():
    return list_productos


@router.get("/{id}")#aqui se llama desde la url para que se muestren los datos de los usuarios
#usando ademas "routers" para ser llamado asi este corriendo el server en main
async def Productos(id: int):
    return list_productos[id]