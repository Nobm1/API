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
    
@app.get("/api/tablaTarifarioEspecifico")
async def ObtenerInformacionTabla():
     # Consulta SQL para obtener datos (por ejemplo)
    consulta = "select * from finanzas.listar_tarifario_especifico();"
    # Ejecutar la consulta utilizando nuestra función
    datos = ejecutar_consulta(consulta)
    # Verificar si hay datos
    if datos:
        datos_formateados = [{
                                "id" : fila[0],
                                "ppu": fila[1],
                                "razon_social": fila[2],
                                "operacion": fila[3],
                                "cop": fila[4],
                                "periodo": fila[5],
                                "tarifa":fila[6],
                                "fecha_de_caducidad": fila[7]
                            } 
                            for fila in datos]
        return datos_formateados
    else:
        raise HTTPException(status_code=404, detail="No se encontraron datos")
    
@app.get("/api/CentroFilter")
async def datos_cop():
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

@app.post("/api/insertDateTe")
async def insertarFechaCaducidad(id:str, fecha_de_caducidad:str):
    try:
        conexion = psycopg2.connect(**parametros_conexion)
        cursor = conexion.cursor()
        consulta = f"UPDATE finanzas.tarifario_especifico SET fecha_de_caducidad='{fecha_de_caducidad}' WHERE id={id};"
        cursor.execute(consulta)
        conexion.commit()
        cursor.close()
        conexion.close()
        print()
        return {"message": "Datos Ingresados Correctamente"}
    except Exception as e: raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/NuevaTarifa")
async def actualizar_estado(id_usuario:str, ids_usuario:str, latitud:str, longitud:str, ppu:int, razon_social:int, operacion:int, centro_operacion:int, periodicidad: int, tarifa: int):
    try:
        conexion = psycopg2.connect(**parametros_conexion)
        cursor = conexion.cursor()
        consulta = f"INSERT INTO finanzas.tarifario_especifico(id_usuario, ids_usuario, latitud, longitud, ppu, razon_social, operacion, centro_operacion, periodicidad, tarifa) VALUES('{id_usuario}','{ids_usuario}','{latitud}','{longitud}',{ppu},{razon_social},{operacion},{centro_operacion},{periodicidad},{tarifa})"
        cursor.execute(consulta)
        conexion.commit()
        cursor.close()
        conexion.close()
        print()
        return {"message": "Datos Ingresados Correctamente"}
    except Exception as e: raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/getOperacion")
async def getOperaciones():
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

@app.get("/api/getCentroOperacion")
async def select_info_cop(id_op: int):
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
async def selectTipoVehiculo():
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

@app.get("/api/getPeriodicidad")
async def ObtenerPeriodo():
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
                                "icono": fila[3]
                            } 
                            for fila in datos]
        return datos_formateados
    else:
        raise HTTPException(status_code=404, detail="No se encontraron datos")

@app.get("/api/CentroFilter")
async def SelectCo():
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

@app.get("/api/Colaborador")
async def SelectRazonSocial():
     # Consulta SQL para obtener datos (por ejemplo)
    consulta = f"""select id, razon_social from transporte.colaborador c"""
    # Ejecutar la consulta utilizando nuestra función
    datos = ejecutar_consulta(consulta)
    # Verificar si hay datos
    if datos:
        datos_formateados = [{
                                "id" : fila[0],
                                "razon_social": fila[1]

                            } 
                            for fila in datos]
        return datos_formateados
    else:
        raise HTTPException(status_code=404, detail="No se encontraron datos")

@app.get("/api/vehiculosXpatente")
async def SelectpatenteFiltrada( id:int):
     # Consulta SQL para obtener datos (por ejemplo)
    consulta = f"""select id, ppu  from transporte.vehiculo v  where razon_id = {id}"""
    # Ejecutar la consulta utilizando nuestra función
    datos = ejecutar_consulta(consulta)
    # Verificar si hay datos
    if datos:
        datos_formateados = [{
                                "id" : fila[0],
                                "ppu": fila[1]

                            } 
                            for fila in datos]
        return datos_formateados
    else:
        raise HTTPException(status_code=404, detail="No se encontraron datos")
    
@app.get("/api/infoTableToSearchTe")
async def Obtener_datos():
     # Consulta SQL para obtener datos (por ejemplo)
    consulta = "SELECT id, operacion, centro_operacion, ppu, periodicidad, tarifa, fecha_de_caducidad FROM finanzas.tarifario_especifico te WHERE fecha_de_caducidad IS NULL;"
    # Ejecutar la consulta utilizando nuestra función
    datos = ejecutar_consulta(consulta)
    # Verificar si hay datos
    if datos:
        datos_formateados = [{
                                "id": fila [0],
                                "operacion" : fila[1],
                                "centro_operacion": fila[2],
                                "tipo_vehiculo":fila[3],
                                "periodicidad":fila[4],
                                "tarifa":fila[5],
                                "fecha_de_caducidad":fila[6]
                            } 
                            for fila in datos]
        return datos_formateados
    else:
        raise HTTPException(status_code=404, detail="No se encontraron datos")


if __name__ == "__main__":
 uvicorn.run(app, host="0.0.0.0", port=8000)