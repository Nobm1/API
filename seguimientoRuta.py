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
    allow_methods=["GET","POST","DELETE"],
    allow_headers=["*"],
)
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


@app.get("/SeguimientoRuta")
async def Obtener_datos():
     # Consulta SQL para obtener datos (por ejemplo)
    consulta = """
            select to_char(rt.fecha_llegada,'HH24:mi') as hora,
                case
                    when lower(rt.estado) in ('entregado','retirado') then 1
                    else 0
                end as estado            
            from beetrack.ruta_transyanez rt
            where rt.identificador_ruta = '42101721'
            and estado notnull
            order by 1 asc"""
    # Ejecutar la consulta utilizando nuestra función
    datos = ejecutar_consulta(consulta)
    # Verificar si hay datos
    if datos:
        datos_formateados = [{
                                "hora" : fila[0],
                                "estado": fila[1]}
                                
                            for fila in datos]
        return datos_formateados
    else:
        raise HTTPException(status_code=404, detail="No se encontraron datos")
    

    
if __name__ == "__main__":
 uvicorn.run(app, host="0.0.0.0", port=8000)
