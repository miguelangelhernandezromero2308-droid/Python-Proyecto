from datetime import datetime
from fastapi import FastAPI, HTTPException
from app.modelos.cliente import Cliente, ClienteCrear, ClienteEditar
from app.modelos.factura import Factura, FacturaCrear, FacturaEditar
from app.modelos.transacciones import Transacciones, TransaccionesCrear, TransaccionesEditar


app = FastAPI()

lista_clientes: list[Cliente] = []
lista_facturas: list[Factura] = []
lista_transacciones: list[Transacciones] = []

@app.get("/clientes", response_model=list[Cliente])
async def Listar_clientes ():
    if len(lista_clientes) == 0:
        return {"clientes": "No hay clientes"}
    else:
        return {"clientes": lista_clientes}

@app.get("/clientes/{id}", response_model=Cliente)
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

@app.put("/facturas/{id}")
def editar_factura(id: int, datos_factura: FacturaEditar):
    factura_editada = None
    
    for indice, factura in enumerate(lista_facturas):
        if factura.id == id:
            datos_dict = datos_factura.model_dump()
            datos_dict["fecha"] = factura.fecha
            datos_dict["cliente"] = factura.cliente
            datos_dict["transacciones"] = factura.transacciones
            factura_editada = Factura.model_validate(datos_dict)
            factura_editada.id = id  
            lista_facturas[indice] = factura_editada
            break
            
    if not factura_editada:
        raise HTTPException(status_code=404, detail="Factura no encontrada para editar")
        
    return {"mensaje": "Factura editada correctamente", "factura": factura_editada}



@app.delete("/facturas/{id}")
def eliminar_factura(id: int):
    for factura in lista_facturas:
        if factura.id == id:
            for transaccion in list(lista_transacciones):
                if transaccion.factura_id == id:
                    lista_transacciones.remove(transaccion)
            lista_facturas.remove(factura)
            return {"mensaje": "La factura y sus transacciones asociadas han sido eliminadas", "factura": factura}
            
    raise HTTPException(status_code=404, detail="Factura no encontrada para eliminar")

#------------ endpoint de transacciones -------------

@app.get("/transacciones", response_model=list[Transacciones])
def listar_transacciones ():
    return lista_transacciones



@app.get("/transacciones/{id}", response_model=Transacciones)
def obtener_transaccion(id: int):
    for transaccion in lista_transacciones:
        if transaccion.id == id:
            return transaccion
    raise HTTPException(status_code=404, detail="Transacción no encontrada")



@app.post("/transacciones", response_model=Transacciones)
def crear_transaccion(datos_transaccion: TransaccionesCrear):
    factura_encontrada = None
    for factura in lista_facturas:
        if factura.id == datos_transaccion.factura_id:
            factura_encontrada = factura
            break
            
    if not factura_encontrada:
        raise HTTPException(status_code=404, detail="La factura especificada no existe")
    nueva_transaccion = Transacciones.model_validate(datos_transaccion.model_dump())
    nueva_transaccion.id = len(lista_transacciones) + 1
    lista_transacciones.append(nueva_transaccion)
    factura_encontrada.transacciones.append(nueva_transaccion)
    
    return nueva_transaccion



@app.put("/transacciones/{id}")
def editar_transaccion(id: int, datos_transaccion: TransaccionesEditar):
    transaccion_editada = None
    
    for indice, transaccion in enumerate(lista_transacciones):
        if transaccion.id == id:
            transaccion_editada = Transacciones.model_validate(datos_transaccion.model_dump())
            transaccion_editada.id = id
            transaccion_editada.factura_id = transaccion.factura_id
            
            lista_transacciones[indice] = transaccion_editada
            break
            
    if not transaccion_editada:
        raise HTTPException(status_code=404, detail="Transacción no encontrada para editar")
    for factura in lista_facturas:
        if factura.id == transaccion_editada.factura_id:
            for indice_t, t_factura in enumerate(factura.transacciones):
                if t_factura.id == id:
                    factura.transacciones[indice_t] = transaccion_editada
                    break
            break

    return {"mensaje": "Transacción editada correctamente", "transaccion": transaccion_editada}



@app.delete("/transacciones/{id}")
def eliminar_transaccion(id: int):
    transaccion_a_eliminar = None

    for transaccion in lista_transacciones:
        if transaccion.id == id:
            transaccion_a_eliminar = transaccion
            lista_transacciones.remove(transaccion)
            break
            
    if not transaccion_a_eliminar:
        raise HTTPException(status_code=404, detail="Transacción no encontrada para eliminar")
    
    for factura in lista_facturas:
        if factura.id == transaccion_a_eliminar.factura_id:
            for t_factura in factura.transacciones:
                if t_factura.id == id:
                    factura.transacciones.remove(t_factura)
                    break
            break
            
    return {"mensaje": "La transacción ha sido eliminada", "transaccion": transaccion_a_eliminar}