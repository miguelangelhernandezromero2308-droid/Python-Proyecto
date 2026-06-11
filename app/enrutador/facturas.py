from fastapi import APIRouter, HTTPException
from datetime import datetime
from ..listas_app import lista_facturas, lista_clientes, lista_transacciones
from app.modelos.factura import Factura, FacturaCrear, FacturaEditar
import app

ruta_facturas = APIRouter()

@ruta_facturas.get("/facturas", response_model=list[Factura])
def listar_facturas ():
    return lista_facturas

@ruta_facturas.get("/facturas/{id}")
def listar_factura (id: int):
    for factura in lista_facturas:
        if factura.id == id:
            return factura
        
@ruta_facturas.post("/facturas/{cliente_id}", response_model=Factura)
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

@ruta_facturas.put("/facturas/{id}")
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



@ruta_facturas.delete("/facturas/{id}")
def eliminar_factura(id: int):
    for factura in lista_facturas:
        if factura.id == id:
            for transaccion in list(lista_transacciones):
                if transaccion.factura_id == id:
                    lista_transacciones.remove(transaccion)
            lista_facturas.remove(factura)
            return {"mensaje": "La factura y sus transacciones asociadas han sido eliminadas", "factura": factura}
            
    raise HTTPException(status_code=404, detail="Factura no encontrada para eliminar")
