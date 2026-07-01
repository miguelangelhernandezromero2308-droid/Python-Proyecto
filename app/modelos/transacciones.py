from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Relationship

from app.modelos.cliente import ClienteBase

class TransaccionesBase(SQLModel):
    Cantidad: int = Field(default=0)
    vr_unitario: float = Field(default=0.0)

class TransaccionesCrear(TransaccionesBase  ):
    factura_id: int 

class TransaccionesEditar(TransaccionesBase):
    pass

class Transacciones(TransaccionesBase, table=True): 
    id : int |None = Field(default=None, primary_key=True)
    factura_id: int |None = Field(default=None, foreign_key="factura.id")