import fastapi
import sqlite3
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# Crea la base de datos
conn = sqlite3.connect("dispositivos.db")

app = fastapi.FastAPI()

class Contacto(BaseModel):
    id : int
    dispositivo : str
    valor : str
    
class Dispositivo(BaseModel):
    valor : str

# Origins
origins = [
    "http://localhost:8080",
    "http://127.0.0.1:5000",
    ##"https://herokufrontend23-2e5ad8e49cc5.herokuapp.com"
]

# Cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/dispositivos")
async def obtener_dispositivos():
    """Obtiene todos los dispositivos."""
    c = conn.cursor()
    c.execute('SELECT * FROM dispositivos;')  # Cambia la consulta para seleccionar los dispositivos
    response = []
    for row in c:
        dispositivo = {"id_dispositivo": row[0], "dispositivo": row[1], "valor": row[2]}
        response.append(dispositivo)
    return response


@app.get("/dispositivos/{id_dispositivo}")
async def obtener_valor_dispositivo(id_dispositivo: int):
    """Obtiene el valor de un dispositivo por su id_dispositivo."""
    c = conn.cursor()
    c.execute('SELECT valor FROM dispositivos WHERE id_dispositivo = ?', (id_dispositivo,))
    valor = c.fetchone()  # Obtiene la primera fila de la consulta
    
    return {"valor": valor[0] if valor else None}  # Devuelve el valor o None si no se encontró el dispositivo

@app.patch("/dispositivos/{id_dispositivo}")
async def actualizar_valor_dispositivo(id_dispositivo: int, contacto: Dispositivo):
    """Actualiza el valor de un dispositivo por su id_dispositivo."""
    c = conn.cursor()
    c.execute('UPDATE dispositivos SET valor = ? WHERE id_dispositivo = ?', (contacto.valor, id_dispositivo))
    conn.commit()
    return {"mensaje": "Valor actualizado"}