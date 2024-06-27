from sqlalchemy.orm import Session
from datetime import datetime
from . import models
from app.encryption import encrypt_data, decrypt_data

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
        'fec_alta': parse_datetime(user['fec_alta'])
    }
    db_user = models.User(**encrypted_user)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session, skip: int = 0, limit: int = 10):
    users = db.query(models.User).offset(skip).limit(limit).all()
    return users
