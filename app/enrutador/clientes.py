from fastapi import APIRouter
from app.modelos.cliente import Cliente, ClienteCrear, ClienteEditar
from ..listas_app import lista_clientes

ruta_clientes = APIRouter()

@ruta_clientes.get("/clientes")
async def listar_clientes():
    return {"Clientes": lista_clientes}

@ruta_clientes.get("/clientes/{id}", response_model=Cliente)
async def listar_cliente (id:int):
    for Cliente in lista_clientes:
        if Cliente.id == id:
            return Cliente

@ruta_clientes.post("/clientes", response_model=Cliente)
async def Crear_cliente (datos_cliente: ClienteCrear):
    #validar el cliente
    cliente_val = Cliente.model_validate(datos_cliente.model_dump())
    #asignar un id al cliente autoincremental
    cliente_val.id = len(lista_clientes) + 1
    #agregar el cliente a la lista de clientes
    lista_clientes.append(cliente_val)
    return cliente_val 

@ruta_clientes.put("/clientes/{id}")
async def editar_cliente (id: int, datos_cliente: ClienteEditar):
    for cliente in lista_clientes:
        if cliente.id == id:
            lista_clientes.remove(cliente)
            # Validar los datos del cliente editado
            cliente_editado = Cliente.model_validate(datos_cliente.model_dump())
            # Asignar el mismo ID al cliente editado
            cliente_editado.id = id
            # Agregar el cliente editado a la lista de clientes
            lista_clientes.append(cliente_editado)
    return{"mensaje": "Cliente editado", "cliente": cliente_editado}

@ruta_clientes.delete("/clientes/{id}")
async def eliminar_cliente (id: int):
    for cliente in lista_clientes:
        if cliente.id == id:
            lista_clientes.remove(cliente)
    return{"mensaje": "el cliente ha sido eliminado correctamente", "cliente": cliente} 