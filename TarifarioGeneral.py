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
    
@app.get("/api/getOperacion")
async def Obtener_datos():
     # Consulta SQL para obtener datos (por ejemplo)
    consulta = "select id, nombre from operacion.modalidad_operacion mo  "
    # Ejecutar la consulta utilizando nuestra función
    datos = ejecutar_consulta(consulta)
    # Verificar si hay datos
    if datos:
        datos_formateados = [{
                                "id" : fila[0],
                                "nombre": fila[1],
                            } 
                            for fila in datos]
        return datos_formateados
    else:
        raise HTTPException(status_code=404, detail="No se encontraron datos")
    
@app.get("/api/infoTableToSearch")
async def Obtener_datos():
     # Consulta SQL para obtener datos (por ejemplo)
    consulta = "SELECT id,operacion, centro_operacion, tipo_vehiculo, capacidad, periodicidad, tarifa, fecha_de_caducidad FROM finanzas.tarifario_general tg WHERE fecha_de_caducidad IS NULL;"
    # Ejecutar la consulta utilizando nuestra función
    datos = ejecutar_consulta(consulta)
    # Verificar si hay datos
    if datos:
        datos_formateados = [{
                                "id": fila [0],
                                "operacion" : fila[1],
                                "centro_operacion": fila[2],
                                "tipo_vehiculo":fila[3],
                                "capacidad":fila[4],
                                "periodicidad":fila[5],
                                "tarifa":fila[6],
                                "fecha_de_caducidad":fila[7]
                            } 
                            for fila in datos]
        return datos_formateados
    else:
        raise HTTPException(status_code=404, detail="No se encontraron datos")
    

@app.get("/api/getCentroOperacion")
async def Obtener_datos(id_op: int):
     # Consulta SQL para obtener datos (por ejemplo)
    consulta = f"""select id,centro from operacion.centro_operacion co where id_op = {id_op}"""
    # Ejecutar la consulta utilizando nuestra función
    datos = ejecutar_consulta(consulta)
    # Verificar si hay datos
    if datos:
        datos_formateados = [{
                                "id" : fila[0],
                                "centro": fila[1],
                            } 
                            for fila in datos]
        return datos_formateados
    else:
        raise HTTPException(status_code=404, detail="No se encontraron datos")

@app.get("/api/getTipoVehiculo")
async def Obtener_datos():
     # Consulta SQL para obtener datos (por ejemplo)
    consulta = f"""select * from transporte.tipo_vehiculo tv """
    # Ejecutar la consulta utilizando nuestra función
    datos = ejecutar_consulta(consulta)
    # Verificar si hay datos
    if datos:
        datos_formateados = [{
                                "id" : fila[0],
                                "tipo": fila[1],
                            } 
                            for fila in datos]
        return datos_formateados
    else:
        raise HTTPException(status_code=404, detail="No se encontraron datos")
    
@app.get("/api/GetCaracteristicasTarifa")
async def Obtener_datos():
     # Consulta SQL para obtener datos (por ejemplo)
    consulta = f"""select id,nombre,valor_inferior,valor_superior,unidad from finanzas.caracteristica_tarifa ct """
    # Ejecutar la consulta utilizando nuestra función
    datos = ejecutar_consulta(consulta)
    # Verificar si hay datos
    if datos:
        datos_formateados = [{
                                "id" : fila[0],
                                "nombre": fila[1],
                                "valor_inferior":fila[2],
                                "valor_superior":fila[3],
                                "unidad": fila[4]
                            } 
                            for fila in datos]
        return datos_formateados
    else:
        raise HTTPException(status_code=404, detail="No se encontraron datos")
    

@app.get("/api/getPeriodicidad")
async def Obtener_datos():
     # Consulta SQL para obtener datos (por ejemplo)
    consulta = f"""select * from finanzas.periodicidad p"""
    # Ejecutar la consulta utilizando nuestra función
    datos = ejecutar_consulta(consulta)
    # Verificar si hay datos
    if datos:
        datos_formateados = [{
                                "id" : fila[0],
                                "periodo": fila[1],
                                "descripcion":fila[2],
                                "icono":fila[3]
                            } 
                            for fila in datos]
        return datos_formateados
    else:
        raise HTTPException(status_code=404, detail="No se encontraron datos")

@app.get("/api/getInfoTable")
async def Obtener_datos():
     # Consulta SQL para obtener datos (por ejemplo)
    consulta = f"""select * from finanzas.listar_tarifario_general();"""
    # Ejecutar la consulta utilizando nuestra función
    datos = ejecutar_consulta(consulta)
    # Verificar si hay datos
    if datos:
        datos_formateados = [{  
                                "id": fila [0],
                                "nombre" : fila[1],
                                "centro": fila[2],
                                "tipo":fila[3],
                                "caracteristica_tarifa":fila[4],
                                "periodo":fila[5],
                                "tarifa":fila[6],
                                "fecha_de_caducidad":fila[7]
                                        

                            } 
                            for fila in datos]
        return datos_formateados
    else:
        raise HTTPException(status_code=404, detail="No se encontraron datos")

@app.get("/api/CentroFilter")
async def Obtener_datos():
     # Consulta SQL para obtener datos (por ejemplo)
    consulta = f"""select id, centro, descripcion from operacion.centro_operacion co"""
    # Ejecutar la consulta utilizando nuestra función
    datos = ejecutar_consulta(consulta)
    # Verificar si hay datos
    if datos:
        datos_formateados = [{
                                "id" : fila[0],
                                "centro": fila[1],
                                "descripcion": fila[2]

                            } 
                            for fila in datos]
        return datos_formateados
    else:
        raise HTTPException(status_code=404, detail="No se encontraron datos")

@app.post("/api/insertDate")
async def actualizar_estado(id:str, fecha_de_caducidad:str):
    try:
        conexion = psycopg2.connect(**parametros_conexion)
        cursor = conexion.cursor()
        consulta = f"UPDATE finanzas.tarifario_general SET fecha_de_caducidad='{fecha_de_caducidad}' WHERE id={id};"
        cursor.execute(consulta)
        conexion.commit()
        cursor.close()
        conexion.close()
        print()
        return {"message": "Datos Ingresados Correctamente"}
    except Exception as e: raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/NuevaTarifa")
async def actualizar_estado(id_usuario:str, ids_usuario:str, latitud:str, longitud:str, operacion:int, centro_operacion:int, tipo_vehiculo:int, capacidad:int, periodicidad: int, tarifa: int):
    try:
        conexion = psycopg2.connect(**parametros_conexion)
        cursor = conexion.cursor()
        consulta = f"INSERT INTO finanzas.tarifario_general(id_usuario, ids_usuario, latitud, longitud, operacion, centro_operacion, tipo_vehiculo, capacidad, periodicidad, tarifa) VALUES('{id_usuario}','{ids_usuario}','{latitud}','{longitud}',{operacion},{centro_operacion},{tipo_vehiculo},{capacidad},{periodicidad},{tarifa})"
        cursor.execute(consulta)
        conexion.commit()
        cursor.close()
        conexion.close()
        print()
        return {"message": "Datos Ingresados Correctamente"}
    except Exception as e: raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
 uvicorn.run(app, host="0.0.0.0", port=8000)