from fastapi import APIRouter, HTTPException, status
from app.modelos.cliente import Cliente, ClienteCrear, ClienteEditar
from ..conexion_bd import Sesion_dependencia
from sqlmodel import select

ruta_clientes = APIRouter()

# 1. LISTAR TODOS LOS CLIENTES
@ruta_clientes.get("/clientes")
async def listar_clientes(sesion: Sesion_dependencia):
    lista_cli = sesion.exec(select(Cliente)).all()
    return lista_cli

# 2. OBTENER UN CLIENTE POR ID
@ruta_clientes.get("/clientes/{id}", response_model=Cliente)
async def listar_cliente(id: int, mi_sesion: Sesion_dependencia):
    
    cliente_encontrado = mi_sesion.get(Cliente, id)
    
    if cliente_encontrado is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Cliente no encontrado"
        )
    
    
    return cliente_encontrado

# 3. CREAR CLIENTE
@ruta_clientes.post("/clientes", response_model=Cliente)
async def Crear_cliente(datos_cliente: ClienteCrear, mi_sesion: Sesion_dependencia):
    cliente_val = Cliente.model_validate(datos_cliente.model_dump())
    mi_sesion.add(cliente_val)
    mi_sesion.commit()
    mi_sesion.refresh(cliente_val)
    return cliente_val 

# 4. EDITAR CLIENTE
@ruta_clientes.put("/clientes/{id}")
async def editar_cliente(id: int, datos_cliente: ClienteEditar, mi_sesion: Sesion_dependencia):
    cliente_bd = mi_sesion.get(Cliente, id)
    if not cliente_bd:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Cliente no encontrado para editar"
        )
    
    datos_nuevos = datos_cliente.model_dump(exclude_unset=True)
    for llave, valor in datos_nuevos.items():
        setattr(cliente_bd, llave, valor)
    
    mi_sesion.add(cliente_bd)
    mi_sesion.commit()
    mi_sesion.refresh(cliente_bd)
    return {"mensaje": "Cliente editado", "cliente": cliente_bd}

# 5. ELIMINAR CLIENTE
@ruta_clientes.delete("/clientes/{id}")
async def eliminar_cliente(id: int, mi_sesion: Sesion_dependencia):
    cliente = mi_sesion.get(Cliente, id)
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Cliente no encontrado para eliminar"
        )
    
    mi_sesion.delete(cliente)
    mi_sesion.commit()
    return {"mensaje": "El cliente ha sido eliminado correctamente", "cliente": cliente}