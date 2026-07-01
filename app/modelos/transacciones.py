from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.modelos.factura import Factura

class TransaccionesBase(SQLModel):
    Cantidad: int = Field(default=0)
    vr_unitario: float = Field(default=0.0)

class TransaccionesCrear(TransaccionesBase):
    factura_id: int 

class TransaccionesEditar(TransaccionesBase):
    pass

class Transacciones(TransaccionesBase, table=True): 
    id: int | None = Field(default=None, primary_key=True)
    factura_id: int | None = Field(default=None, foreign_key="factura.id")
    
    # Relación virtual apuntando correctamente con comillas
    factura: "Factura" = Relationship(back_populates="transacciones")