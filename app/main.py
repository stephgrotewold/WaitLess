from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, crud, database
from app.models import CategoryEnum 
from .database import engine, get_db
from app.auth import get_password_hash, verify_password  # Importar desde auth.py
from datetime import datetime, timedelta

# Inicializar la aplicación
app = FastAPI()

# Crear las tablas en la base de datos
models.Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "¡Bienvenido a WaitLess API!"}

# Registrar un nuevo usuario
@app.post("/register/")
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Verificar si el usuario ya existe
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="El usuario ya está registrado")
    
    # Hashear la contraseña y crear el usuario
    hashed_password = get_password_hash(user.password)
    db_user = models.User(name=user.name, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message": "Usuario registrado exitosamente", "user": db_user}

@app.post("/report/")
def report_wait_time(report: schemas.ReportCreate, db: Session = Depends(get_db)):
    # Verificar si el usuario existe
    db_user = db.query(models.User).filter(models.User.id == report.user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Verificar si el establecimiento existe
    db_establishment = db.query(models.Establishment).filter(models.Establishment.id == report.establishment_id).first()
    if not db_establishment:
        raise HTTPException(status_code=404, detail="Establecimiento no encontrado")
    
    # Verificar si el usuario ya ha hecho un reporte reciente para el mismo establecimiento
    last_report = db.query(models.Report).filter(
        models.Report.user_id == report.user_id,
        models.Report.establishment_id == report.establishment_id
    ).order_by(models.Report.report_time.desc()).first()
    
    if last_report:
        time_difference = datetime.now() - last_report.report_time
        if time_difference < timedelta(minutes=60): 
            raise HTTPException(status_code=400, detail="Solo puedes reportar 1 vez cada hora")
    
    # Crear el nuevo reporte si no hay conflicto
    db_report = models.Report(user_id=report.user_id, establishment_id=report.establishment_id,
                              wait_time=report.wait_time, report_time=datetime.now())
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return {"message": "Reporte enviado exitosamente", "report": db_report}
# Obtener los tiempos de espera de un establecimiento
@app.get("/wait_times/{establishment_id}")
def get_wait_times(establishment_id: int, db: Session = Depends(get_db)):
    wait_times = db.query(models.Report).filter(models.Report.establishment_id == establishment_id).all()
    if not wait_times:
        return {"message": "No hay reportes para este establecimiento"}
    return {"wait_times": wait_times}

# Obtener todos los establecimientos
@app.get("/establishments/")
def get_establishments(db: Session = Depends(get_db)):
    establishments = db.query(models.Establishment).all()
    if not establishments:
        return {"message": "No hay establecimientos registrados"}
    return {"establishments": establishments}

@app.get("/establishments/category/{category}")
def get_establishments_by_category(category: CategoryEnum, db: Session = Depends(get_db)):
    # Filtrar establecimientos por la categoría seleccionada del drop-down
    establishments = db.query(models.Establishment).filter(models.Establishment.category == category.value).all()
    if not establishments:
        return {"message": f"No se encontraron establecimientos en la categoría '{category.value}'"}
    
    return {"establishments": establishments}