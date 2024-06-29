from sqlalchemy import Column, Integer, String, DateTime
from .database import Base

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, index=True)
    codigo_zip = Column(String, index=True)
    credit_card_num = Column(String)
    credit_card_ccv = Column(String)
    cuenta_numero = Column(String)
    direccion = Column(String)
    geo_latitud = Column(String)
    geo_longitud = Column(String)
    color_favorito = Column(String)
    foto_dni = Column(String)
    ip = Column(String)
    auto = Column(String)
    auto_modelo = Column(String)
    auto_tipo = Column(String)
    auto_color = Column(String)
    cantidad_compras_realizadas = Column(Integer)
    avatar = Column(String)
    fec_birthday = Column(DateTime, nullable=True)
    fec_alta = Column(DateTime, nullable=True)
    hashed_password = Column(String)
