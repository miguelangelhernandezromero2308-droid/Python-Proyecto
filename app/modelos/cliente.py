from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING

# Esto le dice a Python que solo importe Factura para revisión de código (Pylance), evitando el bucle
if TYPE_CHECKING:
    from app.modelos.factura import Factura

class ClienteBase(SQLModel):
    nombre: str = Field(default=None)
    email: str = Field(default=None)
    descripcion: str | None = Field(default=None)

class ClienteCrear(ClienteBase):
    pass

class ClienteEditar(ClienteBase):
    pass

class Cliente(ClienteBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    
    
    facturas: list["Factura"] = Relationship(back_populates="cliente")