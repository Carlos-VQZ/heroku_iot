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


"""@app.get("/dispositivos/{id_dispositivo}")
async def obtener_contacto(email: str):
    # Consulta el contacto por su email
    c = conn.cursor()
    c.execute('SELECT * FROM contactos WHERE email = ?', (email,))
    contacto = None
    for row in c:
        contacto = {"email":row[0],"nombre":row[1],"telefono":row[2]}
    return contacto"""