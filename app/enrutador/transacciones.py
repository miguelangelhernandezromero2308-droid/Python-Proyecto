from fastapi import APIRouter, HTTPException, status
from app.modelos.transacciones import Transacciones, TransaccionesCrear, TransaccionesEditar
from app.modelos.factura import Factura
from ..conexion_bd import Sesion_dependencia
from sqlmodel import select

ruta_transacciones = APIRouter()

# 1. LISTAR TODAS LAS TRANSACCIONES
@ruta_transacciones.get("/transacciones", response_model=list[Transacciones])
async def listar_transacciones(sesion: Sesion_dependencia):
    return sesion.exec(select(Transacciones)).all()

# 2. OBTENER UNA TRANSACCIÓN POR ID
@ruta_transacciones.get("/transacciones/{id}", response_model=Transacciones)
async def obtener_transaccion(id: int, sesion: Sesion_dependencia):
    transaccion = sesion.get(Transacciones, id)
    if not transaccion:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transacción no encontrada")
    return transaccion

# 3. CREAR TRANSACCIÓN (Validando que la factura exista primero)
@ruta_transacciones.post("/transacciones", response_model=Transacciones)
async def crear_transaccion(datos_transaccion: TransaccionesCrear, sesion: Sesion_dependencia):
   
    factura_bd = sesion.get(Factura, datos_transaccion.factura_id)
    if not factura_bd:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"No se puede crear la transacción porque la factura con ID {datos_transaccion.factura_id} no existe"
        )
        
    transaccion_val = Transacciones.model_validate(datos_transaccion.model_dump())
    
    sesion.add(transaccion_val)
    sesion.commit()
    sesion.refresh(transaccion_val)
    return transaccion_val

# 4. EDITAR TRANSACCIÓN
@ruta_transacciones.put("/transacciones/{id}")
async def editar_transaccion(id: int, datos_transaccion: TransaccionesEditar, sesion: Sesion_dependencia):
    transaccion_bd = sesion.get(Transacciones, id)
    if not transaccion_bd:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transacción no encontrada para editar")
        
    datos_nuevos = datos_transaccion.model_dump(exclude_unset=True)
    for llave, valor in datos_nuevos.items():
        setattr(transaccion_bd, llave, valor)
        
    sesion.add(transaccion_bd)
    sesion.commit()
    sesion.refresh(transaccion_bd)
    return {"mensaje": "Transacción editada correctamente", "transaccion": transaccion_bd}

# 5. ELIMINAR TRANSACCIÓN
@ruta_transacciones.delete("/transacciones/{id}")
async def eliminar_transaccion(id: int, sesion: Sesion_dependencia):
    transaccion = sesion.get(Transacciones, id)
    if not transaccion:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transacción no encontrada para eliminar")
        
    sesion.delete(transaccion)
    sesion.commit()
    return {"mensaje": "La transacción ha sido eliminada correctamente", "transaccion": transaccion}