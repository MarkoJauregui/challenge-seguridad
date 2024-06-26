from fastapi import FastAPI, Depends, HTTPException
import requests
from sqlalchemy.orm import Session
from . import models, schemas, crud, database

app = FastAPI()

# Crear las tablas en la base de datos
database.Base.metadata.create_all(bind=database.engine)

@app.get("/")
def read_root():
    return {"message": "Welcome to the User API"}

# Endpoint para obtener usuarios desde el API externo y almacenarlos en la base de datos
@app.get("/users")
def get_users(db: Session = Depends(database.get_db)):
    try:
        response = requests.get("https://62433a7fd126926d0c5d296b.mockapi.io/api/v1/usuarios")
        response.raise_for_status()
        users = response.json()
        print("Fetched users:", users)  # Log para ver los datos obtenidos
        for user in users:
            db_user = crud.get_user_by_id(db, user['id'])
            if not db_user:
                print("Creating user:", user)  # Log para ver los datos antes de crear el usuario
                db_user = crud.create_user(db=db, user=user)
        return users
    except requests.exceptions.RequestException as e:
        print("RequestException:", e)  # Log de errores de requests
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        print("Exception:", e)  # Log de errores generales
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para leer usuarios almacenados en la base de datos
@app.get("/internal-users")
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    try:
        users = crud.get_users(db, skip=skip, limit=limit)
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
