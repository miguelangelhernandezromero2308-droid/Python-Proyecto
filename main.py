from datetime import datetime
from fastapi import FastAPI, HTTPException
from modelos.cliente import Cliente, ClienteCrear, ClienteEditar
from modelos.factura import Factura, FacturaCrear, FacturaEditar
from modelos.transacciones import Transacciones, TransaccionesCrear, TransaccionesEditar


app = FastAPI()

lista_clientes: list[Cliente] = []
lista_facturas: list[Factura] = []
lista_transacciones: list[Transacciones] = []

@app.get("/clientes")
async def Listar_clientes ():
    if len(lista_clientes) == 0:
        return {"clientes": "No hay clientes"}
    else:
        return {"clientes": lista_clientes}

@app.get("/clientes/{id}")
async def listar_cliente (id:int):
    for Cliente in lista_clientes:
        if Cliente.id == id:
            return Cliente

@app.post("/clientes", response_model=Cliente)
async def Crear_cliente (datos_cliente: ClienteCrear):
    #validar el cliente
    cliente_val = Cliente.model_validate(datos_cliente.model_dump())
    #asignar un id al cliente autoincremental
    cliente_val.id = len(lista_clientes) + 1
    #agregar el cliente a la lista de clientes
    lista_clientes.append(cliente_val)
    return cliente_val 

@app.put("/clientes/{id}")
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

@app.delete("/clientes/{id}")
async def eliminar_cliente (id: int):
    for cliente in lista_clientes:
        if cliente.id == id:
            lista_clientes.remove(cliente)
    return{"mensaje": "el cliente ha sido eliminado correctamente", "cliente": cliente} 

#------------ endpoint de facturas -------------

@app.get("/facturas", response_model=list[Factura])
def listar_facturas ():
    return lista_facturas

@app.get("/facturas/{id}")
def listar_factura (id: int):
    for factura in lista_facturas:
        if factura.id == id:
            return factura
        
@app.post("/facturas/{cliente_id}", response_model=Factura)
def crear_factura(cliente_id: int, datos_factura: FacturaCrear):
    cliente_encontrado = None
    for cliente in lista_clientes:
        if cliente.id == cliente_id:
            cliente_encontrado = cliente
            break
    if not cliente_encontrado:
        raise HTTPException(status_code=400, detail="Cliente no encontrado")
    
    datos_dict = datos_factura.model_dump()
    datos_dict["fecha"] = datetime.now()
    datos_dict["cliente"] = cliente_encontrado
    datos_dict["transacciones"] = [] 

    factura_val = Factura.model_validate(datos_dict)
    factura_val.id = len(lista_facturas) + 1
    lista_facturas.append(factura_val)
    return factura_val


#------------ endpoint de transacciones -------------

@app.get("/transacciones", response_model=list[Transacciones])
def listar_transacciones ():
    return lista_transacciones


