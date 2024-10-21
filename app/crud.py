from sqlalchemy.orm import Session
from app import models, schemas
from passlib.context import CryptContext
from datetime import datetime

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Crear un nuevo usuario
def create_user(db: Session, user: schemas.UserCreate):
    # Verificar si el usuario ya existe
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        return None  # Podrías lanzar una excepción o manejar esto según tu preferencia
    
    # Crear un nuevo usuario si no existe
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(name=user.name, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Obtener usuario por correo electrónico
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

# Reportar tiempo de espera
def create_report(db: Session, report: schemas.ReportCreate):
    db_report = models.Report(user_id=report.user_id, establishment_id=report.establishment_id,
                              wait_time=report.wait_time, report_time=datetime.now())
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report