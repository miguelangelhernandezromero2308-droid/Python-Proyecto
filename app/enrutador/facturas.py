from fastapi import APIRouter, HTTPException, status
from app.modelos.factura import Factura, FacturaCrear, FacturaEditar
from app.modelos.cliente import Cliente
from ..conexion_bd import Sesion_dependencia
from sqlmodel import select

ruta_facturas = APIRouter()

# 1. LISTAR TODAS LAS FACTURAS
@ruta_facturas.get("/facturas", response_model=list[Factura])
async def listar_facturas(sesion: Sesion_dependencia):
    # Al retornar la lista, FastAPI ejecutará el @computed_field para cada factura automáticamente
    return sesion.exec(select(Factura)).all()

# 2. OBTENER UNA FACTURA POR ID
@ruta_facturas.get("/facturas/{id}", response_model=Factura)
async def obtener_factura(id: int, sesion: Sesion_dependencia):
    factura = sesion.get(Factura, id)
    if not factura:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Factura no encontrada")
    return factura  # Aquí ya se incluye el 'valor_total' calculado desde el modelo

# 3. CREAR FACTURA ASOCIADA A UN CLIENTE
@ruta_facturas.post("/facturas/{cliente_id}", response_model=Factura)
async def crear_factura(cliente_id: int, datos_factura: FacturaCrear, sesion: Sesion_dependencia):
    cliente_bd = sesion.get(Cliente, cliente_id)
    if not cliente_bd:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cliente no encontrado")
    
    datos_dict = datos_factura.model_dump()
    datos_dict["cliente_id"] = cliente_id
    
    # Validación con model_validate
    factura_val = Factura.model_validate(datos_dict)
    
    sesion.add(factura_val)
    sesion.commit()
    sesion.refresh(factura_val)
    return factura_val

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

# 5. ELIMINAR FACTURA
@ruta_facturas.delete("/facturas/{id}")
async def eliminar_factura(id: int, sesion: Sesion_dependencia):
    factura = sesion.get(Factura, id)
    if not factura:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Factura no encontrada para eliminar")
    
    # Buscamos y eliminamos las transacciones asociadas a mano en la BD antes de borrar la factura
    from app.modelos.transacciones import Transacciones
    transacciones_asociadas = sesion.exec(select(Transacciones).where(Transacciones.factura_id == id)).all()
    for transaccion in transacciones_asociadas:
        sesion.delete(transaccion)
        
    sesion.delete(factura)
    sesion.commit()
    return {"mensaje": "La factura y sus transacciones asociadas han sido eliminadas correctamente"}