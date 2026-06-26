from pydantic import BaseModel

class TareaBase(BaseModel):
    titulo: str
    descripcion: str = None
    completada: bool = False

class TareaCreate(TareaBase):
    pass

class Tarea(TareaBase):
    id: int

    class Config:
        from_attributes = True