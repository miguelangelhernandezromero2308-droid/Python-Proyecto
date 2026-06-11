from pydantic import BaseModel

from app.modelos.cliente import ClienteBase

class TransaccionesBase(BaseModel):
    concepto: str
    monto: float  
    descripcion: str | None = None

class TransaccionesCrear(TransaccionesBase  ):
    factura_id: int 

class TransaccionesEditar(TransaccionesBase):
    pass

class Transacciones(TransaccionesBase):
    id : int |None = None
    factura_id: int |None = None