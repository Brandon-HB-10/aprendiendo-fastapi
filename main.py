from fastapi import FastAPI
from database import engine
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def read_root():
    return {"mensaje": "Hola desde FastAPI!!!"}

@app.get("/saludo/{nombre}")
def saludo(nombre: str):
    return {"mensaje": f"Hola {nombre}!"}