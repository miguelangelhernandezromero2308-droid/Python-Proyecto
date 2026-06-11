from datetime import datetime
from fastapi import FastAPI, HTTPException
from app.modelos.cliente import Cliente, ClienteCrear, ClienteEditar
from app.modelos.factura import Factura, FacturaCrear, FacturaEditar
from app.modelos.transacciones import Transacciones, TransaccionesCrear, TransaccionesEditar
from .listas_app import lista_clientes, lista_facturas, lista_transacciones
from .enrutador import clientes
from .enrutador import facturas
from .enrutador import transacciones

app = FastAPI()

app.include_router(clientes.ruta_clientes, tags=["Clientes"])

#------------ endpoint de facturas -------------

app.include_router(facturas.ruta_facturas, tags=["Facturas"])

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