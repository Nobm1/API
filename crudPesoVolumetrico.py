from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
import uvicorn
import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

app = FastAPI()
# Crear los parámetros de conexión usando las variables del .env
parametros_conexion = {
    "host": os.getenv("DB_HOST"),
    "database": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "port": os.getenv("DB_PORT")
}
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST", "DELETE", "GET"],
    allow_headers=["*"],
)

#  pv = Peso volumetrico
class pv(BaseModel):
    sku: str
    descripcion: str
    alto: int | float
    ancho: int | float
    profundidad: int | float
    peso_kg : int | float
    bultos : int
    id_user : int
    ids_user: str

@app.post("/skuPesoVolumetrico/")
async def skuPesoVolumetrico(body: pv):
    try:
        conexion = psycopg2.connect(**parametros_conexion)
        cursor = conexion.cursor()
        consulta = f"INSERT INTO operacion.pv_sku (sku, descripcion, alto, ancho, profundidad, peso_kg, bultos, id_user, ids_user) VALUES ('{body.sku}','{body.descripcion}',{body.alto},{body.ancho},{body.profundidad},{body.peso_kg},{body.bultos},{body.id_user},'{body.ids_user}')"
        cursor.execute(consulta, (body.sku, body.descripcion, body.alto, body.ancho, body.profundidad, body.peso_kg, body.bultos, body.id_user, body.ids_user))
        conexion.commit()
        cursor.close()
        conexion.close()
        print()
        return {"message": "Datos Ingresados Correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def ejecutar_consulta(sql):
    try:
        conexion = psycopg2.connect(**parametros_conexion)
        cursor = conexion.cursor()
        cursor.execute(sql)
        filas = cursor.fetchall()
        cursor.close()
        conexion.close()
        return filas
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/buscar/sku_descripcion")
async def Obtener_datos(sku_descripcion: str):
     # Consulta SQL para obtener datos (por ejemplo)
    consulta = f"select * from operacion.busca_sku_entrada('{sku_descripcion}');"
    # Ejecutar la consulta utilizando nuestra función
    datos = ejecutar_consulta(consulta)
    # Verificar si hay datos
    if datos:
        datos_formateados = [{
                                "sku" : fila[0],
                                "descripcion": fila[1],
                                "bultos" : fila[2],
                                "alto": fila [3],
                                "ancho": fila[4],
                                "profundidad" : fila[5],
                                "peso_kg" : fila[6],
                            } 
                            for fila in datos]
        return datos_formateados
    else:
        raise HTTPException(status_code=404, detail="No se encontraron datos")

@app.get("/Api/mostrarDatosTable")
async def Obtener_datos(sku: str):
     # Consulta SQL para obtener datos (por ejemplo)
    consulta = f"select * from operacion.buscar_sku_o_descripcion('{sku}')"
    # Ejecutar la consulta utilizando nuestra función
    datos = ejecutar_consulta(consulta)
    # Verificar si hay datos
    if datos:
        datos_formateados = [{  
                                "sku": fila[0],
                                "descripcion": fila[1],
                                "alto": fila [2],
                                "ancho": fila[3],
                                "profundidad" : fila[4],
                                "peso_kg" : fila[5],
                                "bultos" : fila[6],
                                "pv": fila[7],
                            } 
                            for fila in datos]
        return datos_formateados
    else:
        raise HTTPException(status_code=404, detail="No se encontraron datos")


if __name__ == "__main__":
 uvicorn.run(app, host="0.0.0.0", port=8000)
