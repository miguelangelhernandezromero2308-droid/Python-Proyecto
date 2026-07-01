from fastapi import APIRouter, HTTPException, status
from app.modelos.factura import Factura, FacturaCrear, FacturaEditar
from app.modelos.cliente import Cliente
from app.modelos.transacciones import Transacciones
from ..conexion_bd import Sesion_dependencia
from sqlmodel import select

ruta_facturas = APIRouter()

# 1. LISTAR TODAS LAS FACTURAS
@ruta_facturas.get("/facturas", response_model=list[Factura])
async def listar_facturas(sesion: Sesion_dependencia):
    lista_fac = sesion.exec(select(Factura)).all()
    return lista_fac

# 2. OBTENER UNA FACTURA POR ID
@ruta_facturas.get("/facturas/{id}")
async def obtener_factura(id: int, sesion: Sesion_dependencia):
    factura = sesion.get(Factura, id)
    if not factura:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Factura no encontrada")
    
    # Calcular el valor_total sumando las transacciones de esta factura de la BD
    transacciones_fac = sesion.exec(select(Transacciones).where(Transacciones.factura_id == id)).all()
    total = sum(t.Cantidad * t.vr_unitario for t in transacciones_fac)
    
    # Retornamos los datos planos más el valor calculado dinámico
    resultado = factura.model_dump()
    resultado["valor_total"] = total
    return resultado

# 3. CREAR FACTURA ASOCIADA A UN CLIENTE
@ruta_facturas.post("/facturas/{cliente_id}", response_model=Factura)
async def crear_factura(cliente_id: int, datos_factura: FacturaCrear, sesion: Sesion_dependencia):
    # Validar que el cliente exista en la base de datos
    cliente_bd = sesion.get(Cliente, cliente_id)
    if not cliente_bd:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cliente no encontrado")
    
    nueva_factura = Factura(cliente_id=cliente_id)
    sesion.add(nueva_factura)
    sesion.commit()
    sesion.refresh(nueva_factura)
    return nueva_factura

# 4. EDITAR FACTURA
@ruta_facturas.put("/facturas/{id}")
async def editar_factura(id: int, datos_factura: FacturaEditar, sesion: Sesion_dependencia):
    factura_bd = sesion.get(Factura, id)
    if not factura_bd:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Factura no encontrada para editar")
    
    datos_nuevos = datos_factura.model_dump(exclude_unset=True)
    for llave, valor in datos_nuevos.items():
        setattr(factura_bd, llave, valor)
        
    sesion.add(factura_bd)
    sesion.commit()
    sesion.refresh(factura_bd)
    return {"mensaje": "Factura editada correctamente", "factura": factura_bd}

# 5. ELIMINAR FACTURA y sus transacciones asociadas
@ruta_facturas.delete("/facturas/{id}")
async def eliminar_factura(id: int, sesion: Sesion_dependencia):
    factura = sesion.get(Factura, id)
    if not factura:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Factura no encontrada para eliminar")
    
    # Eliminar transacciones que dependan de esta factura primero
    transacciones_asociadas = sesion.exec(select(Transacciones).where(Transacciones.factura_id == id)).all()
    for transaccion in transacciones_asociadas:
        sesion.delete(transaccion)
        
    sesion.delete(factura)
    sesion.commit()
    return {"mensaje": "La factura y sus transacciones asociadas han sido eliminadas correctamente"}