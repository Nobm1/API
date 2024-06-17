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

@app.get("/api/modalidad_operacion")
async def Obtener_datos():
     # Consulta SQL para obtener datos (por ejemplo)
    consulta = f"select * from operacion.modalidad_operacion mo "
    # Ejecutar la consulta utilizando nuestra función
    datos = ejecutar_consulta(consulta)
    # Verificar si hay datos
    if datos:
        datos_formateados = [{
                                "nombre": fila [4]
                            } 
                            for fila in datos]
        return datos_formateados
    else:
        raise HTTPException(status_code=404, detail="No se encontraron datos")

@app.get("/api/conductoresList")
async def Obtener_datos():
     # Consulta SQL para obtener datos (por ejemplo)
    consulta = f"select * from transporte.usuarios u where tipo_usuario = '1'"
    # Ejecutar la consulta utilizando nuestra función
    datos = ejecutar_consulta(consulta)
    # Verificar si hay datos
    if datos:
        datos_formateados = [{
                                "nombre_completo": fila [8]
                            } 
                            for fila in datos]
        return datos_formateados
    else:
        raise HTTPException(status_code=404, detail="No se encontraron datos")

@app.get("/api/peonetaList")
async def Obtener_datos():
     # Consulta SQL para obtener datos (por ejemplo)
    consulta = f"select * from transporte.usuarios u where tipo_usuario = '2'"
    # Ejecutar la consulta utilizando nuestra función
    datos = ejecutar_consulta(consulta)
    # Verificar si hay datos
    if datos:
        datos_formateados = [{
                                "nombre_completo": fila [8]
                            } 
                            for fila in datos]
        return datos_formateados
    else:
        raise HTTPException(status_code=404, detail="No se encontraron datos")
    
@app.delete("/api/borrar")
async def eliminar_modalidad(ppu: str):
    # Construir la sentencia SQL de eliminación
    sql = f"DELETE FROM transporte.vehiculo WHERE ppu='{ppu}';"
    # Llamar a la función para ejecutar la sentencia SQL de eliminación
    ejecutar_consulta(sql)
    return {"message": f"Entrada con ID {ppu} eliminada correctamente"}


@app.get("/api/estadoList")
async def Obtener_datos():
     # Consulta SQL para obtener datos (por ejemplo)
    consulta = f"select * from transporte.estado e"
    # Ejecutar la consulta utilizando nuestra función
    datos = ejecutar_consulta(consulta)
    # Verificar si hay datos
    if datos:
        datos_formateados = [{
                                "id": fila [0],
                                "estado": fila[1]
                            } 
                            for fila in datos]
        return datos_formateados
    else:
        raise HTTPException(status_code=404, detail="No se encontraron datos")

@app.get("/api/citacionOperacionFecha")
async def Obtener_datos(fecha: str, id : int):
     # Consulta SQL para obtener datos (por ejemplo)
    consulta = f"select * from mercadolibre.citacion_operacion_fecha('{fecha}', {id});"
    # Ejecutar la consulta utilizando nuestra función
    datos = ejecutar_consulta(consulta)
    # Verificar si hay datos 
    if datos:
        datos_formateados = [{
                                "Id_operacion": fila [0],
                                "operacion": fila[1],
                                "id_cop": fila[2],
                                "nombre_cop": fila [3],
                                "region": fila[4],
                                "region_name": fila[5],
                                "citacion": fila[6],
                                "confirmados": fila[7]

                            } 
                            for fila in datos]
        return datos_formateados
    else:
        raise HTTPException(status_code=404, detail="No se encontraron datos")
    



if __name__ == "__main__":
 uvicorn.run(app, host="0.0.0.0", port=8000)