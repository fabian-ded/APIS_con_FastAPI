from pymongo import MongoClient #se importa el manejo de la base de datos

#base de datos local
#db_client = MongoClient().local #se hace la conecxion con la base de datos, y ahora agregamos .local para que solo en el codigo lo tenga definido y solo sea colocar users y listo

#base de datos remoto
db_client = MongoClient(
    "mongodb+srv://fabian:Fabi05.@cluster0.hpfhwdm.mongodb.net/users?retryWrites=true&w=majority").fabian#se hace la conecxion con la base de datos remoto y ese nombre que pusimos al final ".fabian" es como una carpeta para mongodb donde debe guarde los datos de la tabla "users"