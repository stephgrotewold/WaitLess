from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from .database import Base


# Defining the CategoryEnum
class CategoryEnum(PyEnum):
    RESTAURANTE = "Restaurante"
    MODA = "Moda"
    DEPORTES = "Deportes"
    TECNOLOGIA = "Tecnología"
    ACCESORIOS = "Accesorios"
    BELLEZA = "Belleza"
    JOYERIA = "Joyería"
    CAFETERIA = "Cafetería"
    BANCOS = "Bancos"
    LIBRERIA = "Librería"
    CUIDADO_PERSONAL = "Cuidado Personal"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    last_report_time = Column(DateTime)

class Establishment(Base):
    __tablename__ = "establishments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    category = Column(String, nullable=False)  # Puedes usar Enum si prefieres limitar las opciones
    address = Column(String)

class Report(Base):
    __tablename__ = "reports"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    establishment_id = Column(Integer, ForeignKey("establishments.id"))
    wait_time = Column(Integer)
    report_time = Column(DateTime)

    user = relationship("User")
    establishment = relationship("Establishment")