from pydantic import BaseModel, computed_field
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import TYPE_CHECKING

# Importamos ClienteBase para poder usarlo en el esquema público sin romper el TYPE_CHECKING
from app.modelos.cliente import ClienteBase 

if TYPE_CHECKING:
    from app.modelos.cliente import Cliente
    from app.modelos.transacciones import Transacciones

class FacturaBase(SQLModel):
    fecha: datetime = Field(default_factory=datetime.now)

class FacturaCrear(BaseModel):
    pass

class FacturaEditar(FacturaBase):
    pass


class FacturaPublica(FacturaBase):
    id: int
    cliente_id: int | None
    valor_total: float
    
    cliente: ClienteBase | None = None 

class Factura(FacturaBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    cliente_id: int | None = Field(default=None, foreign_key="cliente.id")
    
    
    cliente: "Cliente" = Relationship(back_populates="facturas")
    transacciones: list["Transacciones"] = Relationship(back_populates="factura")

    @computed_field
    @property
    def valor_total(self) -> float:
        if not self.transacciones:
            return 0.0
        return sum(t.Cantidad * t.vr_unitario for t in self.transacciones)