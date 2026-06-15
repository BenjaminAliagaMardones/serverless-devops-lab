from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import get_db, engine, Base, SessionLocal
from .models import Visitas, Base

app = FastAPI()

Base.metadata.create_all(bind=engine)

db = SessionLocal()
if not db.query(Visitas).filter(Visitas.id == 1).first():
    registro_inical = Visitas(id=1, contador=0)
    db.add(registro_inical)
    db.commit()
db.close()

@app.get("/")
def read_root(db: Session = Depends(get_db)):
    registro = db.query(Visitas).filter(Visitas.id == 1).first()

    registro.contador += 1
    db.commit()
    db.refresh(registro)

    return {
        "mensaje": "Bienvenido a mi lab con AWS, Docker, Terraform y Ansible",
        "vistas": registro.contador
    }