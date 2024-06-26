from sqlalchemy.orm import Session
from datetime import datetime
from . import models

def parse_datetime(date_str):
    try:
        # Intentar diferentes formatos de fecha que podrías encontrar en los datos
        return datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%fZ')
    except ValueError:
        pass
    try:
        return datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%f')
    except ValueError:
        pass
    # Si todos los formatos fallan, retorna None o un valor por defecto
    return None

def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def create_user(db: Session, user: dict):
    db_user = models.User(
        id=user['id'],
        user_name=user['user_name'],
        codigo_zip=user['codigo_zip'],
        credit_card_num=user['credit_card_num'],
        credit_card_ccv=user['credit_card_ccv'],
        cuenta_numero=user['cuenta_numero'],
        direccion=user['direccion'],
        geo_latitud=user['geo_latitud'],
        geo_longitud=user['geo_longitud'],
        color_favorito=user['color_favorito'],
        foto_dni=user['foto_dni'],
        ip=user['ip'],
        auto=user['auto'],
        auto_modelo=user['auto_modelo'],
        auto_tipo=user['auto_tipo'],
        auto_color=user['auto_color'],
        cantidad_compras_realizadas=user['cantidad_compras_realizadas'],
        avatar=user['avatar'],
        fec_birthday=parse_datetime(user['fec_birthday']),
        fec_alta=parse_datetime(user['fec_alta'])
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.User).offset(skip).limit(limit).all()
