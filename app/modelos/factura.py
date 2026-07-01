from pydantic import BaseModel, computed_field
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from app.modelos.cliente import Cliente
from app.modelos.transacciones import Transacciones


class FacturaBase(SQLModel):
    fecha: datetime = Field(default_factory=datetime.now)
    #cliente: Cliente | None = None
    #transacciones: list[Transacciones] = []

    @computed_field
    @property
    def valor_total(self) -> float:
    #    total = 0.0     
    #    for transaccion in self.transacciones:
    #        total += transaccion.monto
    #    return total
        return 0.0

class FacturaCrear(BaseModel):
    pass

class FacturaEditar(FacturaBase):
    pass

class Factura(FacturaBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    cliente_id: int = Field(default=None, foreign_key="cliente.id")