from datetime import datetime
from fastapi import FastAPI, HTTPException
from app.modelos.cliente import Cliente, ClienteCrear, ClienteEditar
from app.modelos.factura import Factura, FacturaCrear, FacturaEditar
from app.modelos.transacciones import Transacciones, TransaccionesCrear, TransaccionesEditar
from .listas_app import lista_clientes, lista_facturas, lista_transacciones
from .enrutador import clientes
from .enrutador import facturas
from .enrutador import transacciones
from .conexion_bd import crear_tablas

app = FastAPI(lifespan=crear_tablas)

app.include_router(clientes.ruta_clientes, tags=["Clientes"])

#------------ endpoint de facturas -------------

app.include_router(facturas.ruta_facturas, tags=["Facturas"])

#------------ endpoint de transacciones -------------

app.include_router(transacciones.ruta_transacciones, tags=["Transacciones"])