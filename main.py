from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, get_db
import models, schemas
from ia import preguntar_a_claude
from pydantic import BaseModel

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Crear tarea
@app.post("/tareas", response_model=schemas.Tarea)
def crear_tarea(tarea: schemas.TareaCreate, db: Session = Depends(get_db)):
    nueva_tarea = models.Tarea(**tarea.model_dump())
    db.add(nueva_tarea)
    db.commit()
    db.refresh(nueva_tarea)
    return nueva_tarea

# Obtener todas las tareas
@app.get("/tareas", response_model=list[schemas.Tarea])
def obtener_tareas(db: Session = Depends(get_db)):
    return db.query(models.Tarea).all()

# Obtener una tarea
@app.get("/tareas/{tarea_id}", response_model=schemas.Tarea)
def obtener_tarea(tarea_id: int, db: Session = Depends(get_db)):
    tarea = db.query(models.Tarea).filter(models.Tarea.id == tarea_id).first()
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return tarea

# Actualizar tarea
@app.put("/tareas/{tarea_id}", response_model=schemas.Tarea)
def actualizar_tarea(tarea_id: int, tarea: schemas.TareaCreate, db: Session = Depends(get_db)):
    db_tarea = db.query(models.Tarea).filter(models.Tarea.id == tarea_id).first()
    if not db_tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    for key, value in tarea.model_dump().items():
        setattr(db_tarea, key, value)
    db.commit()
    db.refresh(db_tarea)
    return db_tarea

# Eliminar tarea
@app.delete("/tareas/{tarea_id}")
def eliminar_tarea(tarea_id: int, db: Session = Depends(get_db)):
    tarea = db.query(models.Tarea).filter(models.Tarea.id == tarea_id).first()
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    db.delete(tarea)
    db.commit()
    return {"mensaje": "Tarea eliminada"}


class Pregunta(BaseModel):
    mensaje: str

@app.post("/chat")
def chat(pregunta: Pregunta):
    respuesta = preguntar_a_claude(pregunta.mensaje)
    return {"respuesta": respuesta}