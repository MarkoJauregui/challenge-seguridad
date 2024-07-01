from fastapi import FastAPI, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from . import models, schemas, crud, database
from .encryption import encrypt_data, decrypt_data
from .auth import get_current_user, create_access_token
from fastapi.security import OAuth2PasswordRequestForm
import logging
import requests
from typing import List

app = FastAPI()

# Configurar el registro de errores
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

# Crear las tablas en la base de datos
models.Base.metadata.create_all(bind=database.engine)

@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de Usuarios"}

@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(db: Session = Depends(database.get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Nombre de usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

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
        return {"message": "Usuarios obtenidos y almacenados exitosamente."}
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error("Error al obtener o almacenar usuarios", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/internal-users", response_model=List[schemas.User])
def read_internal_users(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db), current_user: schemas.InternalUser = Depends(get_current_user)):
    if current_user.role.name != "admin":
        raise HTTPException(status_code=403, detail="Permisos insuficientes")
    try:
        users = crud.get_users(db, skip=skip, limit=limit)
        decrypted_users = []
        for user in users:
            try:
                decrypted_user = user.__dict__.copy()
                decrypted_user['credit_card_num'] = decrypt_data(user.credit_card_num)
                decrypted_user['credit_card_ccv'] = decrypt_data(user.credit_card_ccv)
                decrypted_user['cuenta_numero'] = decrypt_data(user.cuenta_numero)
                if 'role_id' not in decrypted_user or decrypted_user['role_id'] is None:
                    decrypted_user['role_id'] = 2  # Asigna el role_id de "usuario" por defecto
                decrypted_users.append(decrypted_user)
            except Exception as e:
                logger.error(f"Error al descifrar datos para el usuario con ID {user.id}: {e}", exc_info=True)
                raise HTTPException(status_code=500, detail=f"Error al descifrar datos para el usuario con ID {user.id}")
        return decrypted_users
    except Exception as e:
        logger.error("Error al leer usuarios internos", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error Interno del Servidor: {str(e)}")

@app.post("/encrypt")
async def encrypt(request: Request):
    request_data = await request.json()
    data = request_data.get('data')
    if not data:
        raise HTTPException(status_code=400, detail="No se proporcionaron datos")
    encrypted_data = encrypt_data(data)
    return {"encrypted_data": encrypted_data}

@app.post("/decrypt")
async def decrypt(request: Request):
    request_data = await request.json()
    token = request_data.get('token')
    if not token:
        raise HTTPException(status_code=400, detail="No se proporcionó token")
    decrypted_data = decrypt_data(token)
    return {"decrypted_data": decrypted_data}
