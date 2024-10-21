from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class ReportCreate(BaseModel):
    user_id: int
    establishment_id: int
    wait_time: int

class CategoryEnum(str, Enum):
    moda = "Moda"
    restaurante = "Restaurante"
    cafeteria = "Cafeteria"
    deportes = "Deportes"
    tecnologia = "Tecnologia"
    joyeria = "Joyeria"
    bancos = "Bancos"
    accesorios = "Accesorios"
    cuidado_personal = "Cuidado Personal"
    cine = "Cine"
    libreria = "Libreria"

class EstablishmentCreate(BaseModel):
    name: str
    category: CategoryEnum
    address: str