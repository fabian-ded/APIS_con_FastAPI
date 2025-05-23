#practicamente este esquema es el que se encarga de traer los datos que mongoDB ya guardo y los trae y hace la logica para que FastAPI lo comprenda

def user_schema(user) -> dict:
    return {"id": str(user["_id"]), #MongoDB guarda el ID con el nombre "_id", y es un tipo especial (ObjectId) que FastAPI no entiende directamente por eso
                                    #Aquí lo convertimos en un texto (str(...)) y lo llamamos simplemente id, para que lo entiensa fastAPI
            "username": user["username"],
            "email": user["email"]}