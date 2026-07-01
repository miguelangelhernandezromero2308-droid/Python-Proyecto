from sqlmodel import SQLModel, Session, create_engine
from typing import Annotated
from fastapi import FastAPI, Depends

nombre_bd = "bd_clientes.sqlite3"
url_bd = f"sqlite:///{nombre_bd}"

motor_db = create_engine(url_bd, connect_args={"check_same_thread": False})

def crear_tablas(app: FastAPI):
    SQLModel.metadata.create_all(motor_db)
    yield

def obtener_sesion():
    with Session(motor_db) as mi_sesion:
        yield mi_sesion

# CORREGIDO: Unido con guion bajo (_) para que Python lo pueda importar sin errores
Sesion_dependencia = Annotated[Session, Depends(obtener_sesion)]