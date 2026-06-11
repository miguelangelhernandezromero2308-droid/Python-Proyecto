from pydantic import BaseModel, computed_field
from datetime import datetime
from app.modelos.cliente import Cliente
from app.modelos.transacciones import Transacciones

class FacturaBase(BaseModel):
    fecha: datetime | None = None
    cliente: Cliente | None = None
    transacciones: list[Transacciones] = []

    @computed_field
    @property
    def valor_total(self) -> float:
        total = 0.0     
        for transaccion in self.transacciones:
            total += transaccion.monto
        return total

class FacturaCrear(BaseModel):
    pass

class FacturaEditar(FacturaBase):
    pass

class Factura(FacturaBase):
    id: int | None = None