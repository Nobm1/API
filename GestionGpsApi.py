from fastapi import FastAPI,HTTPException
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
from pydantic import BaseModel
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
    
@app.get("/api/getInfoTable")
async def Obtener_datos():
     # Consulta SQL para obtener datos (por ejemplo)
    consulta = "select * from transporte.obtener_informacion_gps();"
    # Ejecutar la consulta utilizando nuestra función
    datos = ejecutar_consulta(consulta)
    # Verificar si hay datos
    if datos:
        datos_formateados = [{
                                "id_gps" : fila[0],
                                "ppu": fila[1],
                                "razon_social": fila [2],
                                "rut": fila[3],
                                "region" : fila[4],
                                "gps" : fila[5],
                                "fec_instalacion":fila[6],
                                "oc_instalacion":fila[7],
                                "fec_baja": fila[8],
                                "oc_baja" : fila[9],
                                "monto": fila[10],
                                "descontado": fila[11],
                                "devuelto": fila[12],
                                "datos_varios": fila[13]

                            } 
                            for fila in datos]
        return datos_formateados
    else:
        raise HTTPException(status_code=404, detail="No se encontraron datos")

@app.post("/api/oc_instalación")
async def actualizar_estado(oc_instalacion:str, id: int):
    try:
        conexion = psycopg2.connect(**parametros_conexion)
        cursor = conexion.cursor()
        consulta = f"UPDATE transporte.gps SET  oc_instalacion='{oc_instalacion}' WHERE id='{id}'"
        cursor.execute(consulta)
        conexion.commit()
        cursor.close()
        conexion.close()
        print()
        return {"message": "Datos Ingresados Correctamente"}
    except Exception as e: raise HTTPException(status_code=500, detail=str(e))



@app.post("/api/oc_baja")
async def actualizar_estado(oc_baja:str, id: int):
    try:
        conexion = psycopg2.connect(**parametros_conexion)
        cursor = conexion.cursor()
        consulta = f"UPDATE transporte.gps SET  oc_baja='{oc_baja}' WHERE id='{id}'"
        cursor.execute(consulta)
        conexion.commit()
        cursor.close()
        conexion.close()
        print()
        return {"message": "Datos Ingresados Correctamente"}
    except Exception as e: raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/monto")
async def actualizar_estado(monto:str, id: int):
    try:
        conexion = psycopg2.connect(**parametros_conexion)
        cursor = conexion.cursor()
        consulta = f"UPDATE transporte.gps SET  monto='{monto}' WHERE id='{id}'"
        cursor.execute(consulta)
        conexion.commit()
        cursor.close()
        conexion.close()
        print()
        return {"message": "Datos Ingresados Correctamente"}
    except Exception as e: raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/descontado")
async def actualizar_estado(descontado:bool, id: int):
    try:
        conexion = psycopg2.connect(**parametros_conexion)
        cursor = conexion.cursor()
        consulta = f"UPDATE transporte.gps SET  descontado={descontado} WHERE id='{id}'"
        cursor.execute(consulta)
        conexion.commit()
        cursor.close()
        conexion.close()
        print()
        return {"message": "Datos Ingresados Correctamente"}
    except Exception as e: raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/devuelto")
async def actualizar_estado(devuelto:bool, id: int):
    try:
        conexion = psycopg2.connect(**parametros_conexion)
        cursor = conexion.cursor()
        consulta = f"UPDATE transporte.gps SET  devuelto={devuelto} WHERE id='{id}'"
        cursor.execute(consulta)
        conexion.commit()
        cursor.close()
        conexion.close()
        print()
        return {"message": "Datos Ingresados Correctamente"}
    except Exception as e: raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
 uvicorn.run(app, host="0.0.0.0", port=8000)