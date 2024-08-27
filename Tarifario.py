from fastapi import FastAPI,HTTPException
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
from pydantic import BaseModel
import uvicorn

app = FastAPI()
# Parámetros de conexión a la base de datos
parametros_conexion = {
    "host": "44.199.104.254",
    "database": "postgres",
    "user": "wms_readonly",
    "password": "TY2022#",
    "port" : "5432"
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
    
@app.get("/api/infoTarifas")
async def Obtener_datos():
     # Consulta SQL para obtener datos (por ejemplo)
    consulta = "select nombre, valor_inferior, valor_superior, unidad from finanzas.caracteristica_tarifa ct "
    # Ejecutar la consulta utilizando nuestra función
    datos = ejecutar_consulta(consulta)
    # Verificar si hay datos
    if datos:
        datos_formateados = [{
                                "nombre" : fila[0],
                                "valor_inferior": fila[1],
                                "valor_superior": fila [2],
                                "unidad": fila[3],
                            } 
                            for fila in datos]
        return datos_formateados
    else:
        raise HTTPException(status_code=404, detail="No se encontraron datos")
    

@app.get("/api/TipoUnidad")
async def Obtener_datos():
     # Consulta SQL para obtener datos (por ejemplo)
    consulta = "select * from finanzas.tipo_unidad tu "
    # Ejecutar la consulta utilizando nuestra función
    datos = ejecutar_consulta(consulta)
    # Verificar si hay datos
    if datos:
        datos_formateados = [{
                                "id" : fila[0],
                                "unidad": fila[1],
                                "campo_vehiculo": fila [2],
                                "prioridad": fila[3],
                            } 
                            for fila in datos]
        return datos_formateados
    else:
        raise HTTPException(status_code=404, detail="No se encontraron datos")
    

@app.post("/api/NuevaTarifa")
async def actualizar_estado(id_usuario:str, ids_usuario: str, nombre:str, valor_inferior:int, valor_superior:int, unidad:int):
    try:
        conexion = psycopg2.connect(**parametros_conexion)
        cursor = conexion.cursor()
        consulta = f"INSERT INTO finanzas.caracteristica_tarifa (id_usuario, ids_usuario, nombre, valor_inferior, valor_superior, unidad) VALUES('{id_usuario}','{ids_usuario}','{nombre}',{valor_inferior},{valor_superior},{unidad})"
        cursor.execute(consulta)
        conexion.commit()
        cursor.close()
        conexion.close()
        print()
        return {"message": "Datos Ingresados Correctamente"}
    except Exception as e: raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
 uvicorn.run(app, host="0.0.0.0", port=8000)