from sqlmodel import SQLModel, Session, create_engine
from typing import Annotated
from fastapi import FastAPI, Depends

# nombre de la base datos
nombre_bd = "bd_clientes.sqlite3"

# conexion a la bd, con una URL (direccion)
url_bd = f"sqlite:///{nombre_bd}"

# motor de base de datos
motor_db = create_engine(url_bd)

#definir metodo para crear las tablas
def crear_tablas(app: FastAPI):
    SQLModel.metadata.create_all(motor_db)
    yield #no hay nada para retornar o ejecutar

#definir el metodo para la sesion
def obtener_sesion():
    with Session(motor_db) as mi_sesion:
        yield mi_sesion



# Definir la dependencia, y esto registra mi sesion
Sesion_dependencia = Annotated[Session, Depends(obtener_sesion)]