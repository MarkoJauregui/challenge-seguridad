from sqlalchemy.orm import Session
from datetime import datetime
from . import models, schemas
from app.encryption import encrypt_data
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def parse_datetime(date_str):
    try:
        return datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%fZ')
    except ValueError:
        pass
    try:
        return datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%f')
    except ValueError:
        pass
    return None

def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def create_user(db: Session, user: dict):
    encrypted_user = {
        'id': user['id'],
        'user_name': user['user_name'],
        'codigo_zip': user['codigo_zip'],
        'credit_card_num': encrypt_data(user['credit_card_num']),
        'credit_card_ccv': encrypt_data(user['credit_card_ccv']),
        'cuenta_numero': encrypt_data(user['cuenta_numero']),
        'direccion': user['direccion'],
        'geo_latitud': str(user['geo_latitud']),
        'geo_longitud': str(user['geo_longitud']),
        'color_favorito': user['color_favorito'],
        'foto_dni': user['foto_dni'],
        'ip': user['ip'],
        'auto': user['auto'],
        'auto_modelo': user['auto_modelo'],
        'auto_tipo': user['auto_tipo'],
        'auto_color': user['auto_color'],
        'cantidad_compras_realizadas': user['cantidad_compras_realizadas'],
        'avatar': user['avatar'],
        'fec_birthday': parse_datetime(user['fec_birthday']),
        'fec_alta': parse_datetime(user['fec_alta']),
        'role_id': 2  # Asigna el role_id de "usuario" por defecto
    }
    db_user = models.User(**encrypted_user)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.User).offset(skip).limit(limit).all()

def get_internal_user_by_username(db: Session, username: str):
    return db.query(models.InternalUser).filter(models.InternalUser.username == username).first()

def create_internal_user(db: Session, user: schemas.InternalUserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.InternalUser(
        username=user.username,
        hashed_password=hashed_password,
        role_id=user.role_id
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, username: str, password: str):
    user = get_internal_user_by_username(db, username)
    if not user:
        return False
    if not pwd_context.verify(password, user.hashed_password):
        return False
    return user
