from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class Tarea(Base):
    __tablename__ = "tareas"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    descripcion = Column(String)
    completada = Column(Boolean, default=False)