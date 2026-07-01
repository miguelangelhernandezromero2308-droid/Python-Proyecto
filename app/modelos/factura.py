from pydantic import BaseModel, computed_field
from sqlmodel import SQLModel, Field
from datetime import datetime

class FacturaBase(SQLModel):
    fecha: datetime = Field(default_factory=datetime.now)

class FacturaCrear(BaseModel):
    pass

class FacturaEditar(FacturaBase):
    pass

class Factura(FacturaBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    cliente_id: int | None = Field(default=None, foreign_key="cliente.id")