from pydantic import BaseModel, computed_field
from datetime import date, datetime
from modelos.cliente import Cliente
from modelos.transacciones import Transacciones, TransaccionesBase

class FacturaBase(BaseModel):
    
    fecha: date
    cliente: Cliente
    transacciones: list[Transacciones] = []

    @computed_field
    @property
    def valor_total(self) -> float:
        
        total = 0.0     
        for transaccion in self.transacciones:
            total += transaccion.monto
        return total

class FacturaCrear(FacturaBase):
    pass

class FacturaEditar(FacturaBase):
    pass

class Factura(FacturaBase):
    id : int |None = None
