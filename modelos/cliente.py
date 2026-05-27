from pydantic import BaseModel

class ClienteBase(BaseModel):
    nombre: str
    edad: str
    descripcion: str |None 

class ClienteCrear(ClienteBase):
    pass

class ClienteEditar(ClienteBase):
    pass

class Cliente(ClienteBase):
    id : int |None = None