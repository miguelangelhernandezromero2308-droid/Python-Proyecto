from pydantic import BaseModel, computed_field
from sqlmodel import SQLModel, Field, Session, select
from datetime import datetime
from app.modelos.transacciones import Transacciones
from app.conexion_bd import motor_db

class FacturaBase(SQLModel):
    # Usamos datetime para manejar la fecha de manera correcta en la base de datos
    fecha: datetime = Field(default_factory=datetime.now)

class FacturaCrear(BaseModel):
    pass

class FacturaEditar(FacturaBase):
    pass

class Factura(FacturaBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    cliente_id: int | None = Field(default=None, foreign_key="cliente.id")

    # Calculamos el valor total buscando manualmente en la BD sin usar Relationship
    @computed_field
    @property
    def valor_total(self) -> float:
        if self.id is None:
            return 0.0
        
        # Abrimos una sesión rápida para consultar la tabla de transacciones
        with Session(motor_db) as sesion_interna:
            declaracion = select(Transacciones).where(Transacciones.factura_id == self.id)
            transacciones_factura = sesion_interna.exec(declaracion).all()
            
            # Sumamos cantidad por valor unitario (puedes cambiar 'vr_unitario' por 'monto' si tu tabla usa esa columna)
            return sum(t.Cantidad * t.vr_unitario for t in transacciones_factura)