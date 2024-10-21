import csv
from sqlalchemy.orm import Session
from app import models, database

def populate_establishments_from_csv(file_path: str, db: Session):
    with open(file_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            establecimiento = models.Establishment(
            name=row['name'], 
            category=row['category'], 
            address=row['address']
        )
            db.add(establecimiento)
        db.commit()

# Crear la sesión de base de datos y ejecutar la función
db = database.SessionLocal()
populate_establishments_from_csv('/Users/stephgrotewold/Desktop/UFM/OCTAVO/REPOS/WaitLess/establecimientos.csv', db)
db.close()