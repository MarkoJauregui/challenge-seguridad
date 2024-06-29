from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, crud, database
from app.encryption import encrypt_data, decrypt_data
import logging
import requests
from typing import List

app = FastAPI()

# Configurar el registro de errores
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

# Crear las tablas en la base de datos
database.Base.metadata.create_all(bind=database.engine)

@app.get("/")
def read_root():
    return {"message": "Welcome to the User API"}

@app.get("/users")
def get_users(db: Session = Depends(database.get_db)):
    try:
        response = requests.get("https://62433a7fd126926d0c5d296b.mockapi.io/api/v1/usuarios")
        response.raise_for_status()
        users = response.json()
        for user in users:
            db_user = crud.get_user_by_id(db, user['id'])
            if not db_user:
                encrypted_user = user.copy()
                encrypted_user['credit_card_num'] = encrypt_data(user['credit_card_num'])
                encrypted_user['credit_card_ccv'] = encrypt_data(user['credit_card_ccv'])
                encrypted_user['cuenta_numero'] = encrypt_data(user['cuenta_numero'])
                db_user = crud.create_user(db=db, user=encrypted_user)
        return {"message": "Users fetched and stored successfully."}
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error("Error fetching or storing users", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/internal-users", response_model=List[schemas.User])
def read_internal_users(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    try:
        users = crud.get_users(db, skip=skip, limit=limit)
        decrypted_users = []
        for user in users:
            try:
                decrypted_user = user.__dict__.copy()
                decrypted_user['credit_card_num'] = decrypt_data(user.credit_card_num)
                decrypted_user['credit_card_ccv'] = decrypt_data(user.credit_card_ccv)
                decrypted_user['cuenta_numero'] = decrypt_data(user.cuenta_numero)
                decrypted_users.append(decrypted_user)
            except Exception as e:
                logger.error(f"Error decrypting data for user ID {user.id}: {e}", exc_info=True)
                raise HTTPException(status_code=500, detail=f"Error decrypting data for user ID {user.id}")
        return decrypted_users
    except Exception as e:
        logger.error("Error reading internal users", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
