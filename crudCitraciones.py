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

class agregarPatente(BaseModel):
    id_user : int
    ids_user: str
    fecha: str
    id_ppu : int
    id_operacion : int
    id_centro_op : int
    estado : int
    tipo_ruta : int

class updateApp(BaseModel):
    id: int
    estado: bool
    fecha: str

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
async def Obtener_datos(fecha:str):
     # Consulta SQL para obtener datos (por ejemplo)
    consulta = f"select u.id, u.nombre_completo from transporte.usuarios u where u.tipo_usuario = 1 AND u.id NOT IN (select id_driver FROM mercadolibre.citacion c WHERE fecha = '{fecha}'::date and c.id_driver notnull);"
    # Ejecutar la consulta utilizando nuestra función
    datos = ejecutar_consulta(consulta)
    # Verificar si hay datos
    if datos:
        datos_formateados = [{
                                "id": fila[0],
                                "nombre_completo": fila [1]
                            } 
                            for fila in datos]
        return datos_formateados
    else:
        raise HTTPException(status_code=404, detail="No se encontraron datos")

@app.get("/api/peonetaList")
async def Obtener_datos(fecha:str):
     # Consulta SQL para obtener datos (por ejemplo)
    consulta = f"select u.id, u.nombre_completo from transporte.usuarios u where u.tipo_usuario = 2 AND u.id NOT in (select id_peoneta FROM mercadolibre.citacion c WHERE fecha = '{fecha}'::date and c.id_peoneta notnull);"
    # Ejecutar la consulta utilizando nuestra función
    datos = ejecutar_consulta(consulta)
    # Verificar si hay datos
    if datos:
        datos_formateados = [{
                                "id": fila[0],
                                "nombre_completo": fila [1]
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
                                "confirmados": fila[7],
                                "pendientes": fila[8],
                                "rechazadas": fila[9],
                                "ambulancia": fila[10]

                            } 
                            for fila in datos]
        return datos_formateados
    else:
        raise HTTPException(status_code=404, detail="No se encontraron datos")
     

def ejecutar_delete(sql):
    try:
        # Conexión a la base de datos PostgreSQL
        conexion = psycopg2.connect(**parametros_conexion)
        cursor = conexion.cursor()
        # Ejecutar la sentencia SQL de eliminación
        cursor.execute(sql)
        conexion.commit()
        cursor.close()
        conexion.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.delete("/api/borrar")
async def eliminar_modalidad(id_ppu: str):
    # Construir la sentencia SQL de eliminación
    sql = f"DELETE FROM mercadolibre.citacion WHERE id_ppu ='{id_ppu}';"
    # Llamar a la función para ejecutar la sentencia SQL de eliminación
    ejecutar_delete(sql)
    return {"message": f"Entrada con ID {id_ppu} eliminada correctamente"}


@app.get("/api/estadoList")
async def Obtener_datos():
     # Consulta SQL para obtener datos (por ejemplo)
    consulta = f"select * from mercadolibre.estados_citacion ec"
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

@app.get("/api/estadoCitacion")
async def Obtener_datos():
     # Consulta SQL para obtener datos (por ejemplo)
    consulta = f"select * from mercadolibre.estados_citacion ec"
    # Ejecutar la consulta utilizando nuestra función
    datos = ejecutar_consulta(consulta)
    # Verificar si hay datos 
    if datos:
        datos_formateados = [{
                                "id": fila [0],
                                "estado": fila[1],
                                

                            } 
                            for fila in datos]
        return datos_formateados
    else:
        raise HTTPException(status_code=404, detail="No se encontraron datos")
    
@app.get("/api/citacion_cop")
async def Obtener_datos(fecha: str, op : int, cop : int):
     # Consulta SQL para obtener datos (por ejemplo)
    consulta = f"select * from mercadolibre.recupera_citacion_cop('{fecha}',{op},{cop})"
    # Ejecutar la consulta utilizando nuestra función
    datos = ejecutar_consulta(consulta)
    # Verificar si hay datos 
    if datos:
        datos_formateados = [{
                                "id_ppu": fila [0],
                                "ppu": fila[1],
                                "ruta_meli": fila[2],
                                "tipo_ruta":fila[3],
                                "estado": fila [4],
                                "id_driver":fila[5],
                                "nombre_driver": fila[6],
                                "id_peoneta": fila [7],
                                "nombre_peoneta":fila[8]

                            } 
                            for fila in datos]
        return datos_formateados
    else:
        raise HTTPException(status_code=404, detail="No se encontraron datos")
    
    
    
@app.post("/api/agregarpatente/")
async def agregarPatente(body: agregarPatente):
    try:
        conexion = psycopg2.connect(**parametros_conexion)
        cursor = conexion.cursor()
        consulta = f"INSERT INTO mercadolibre.citacion (id_user, ids_user, fecha, id_ppu, id_operacion, id_centro_op, tipo_ruta, estado) VALUES ({body.id_user},'{body.ids_user}','{body.fecha}',{body.id_ppu},{body.id_operacion},{body.id_centro_op},{body.tipo_ruta},{body.estado})"
        cursor.execute(consulta, ({body.id_user},{body.ids_user},{body.fecha},{body.id_ppu},{body.id_operacion},{body.id_centro_op},{body.tipo_ruta},{body.estado}))
        conexion.commit()
        cursor.close()
        conexion.close()
        print()
        return {"message": "Datos Ingresados Correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/api/actualizar_estadoPpu")
async def actualizar_estado(estado: int, id_ppu : int, fecha:str):
    try:
        conexion = psycopg2.connect(**parametros_conexion)
        cursor = conexion.cursor()
        consulta = f"UPDATE mercadolibre.citacion SET estado={estado} WHERE fecha='{fecha}' AND id_ppu={id_ppu}"
        cursor.execute(consulta)
        conexion.commit()
        cursor.close()
        conexion.close()
        print()
        return {"message": "Datos Ingresados Correctamente"}
    except Exception as e: raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/nombreCitacion")
async def Obtener_datos(id_estado: int):
     # Consulta SQL para obtener datos (por ejemplo)
    consulta = f"select estado from mercadolibre.estados_citacion ec where id = {id_estado};"
    # Ejecutar la consulta utilizando nuestra función
    datos = ejecutar_consulta(consulta)
    # Verificar si hay datos 
    if datos:
        datos_formateados = [{
                                "estado": fila[0]

                            } 
                            for fila in datos]
        return datos_formateados
    else:
        raise HTTPException(status_code=404, detail="No se encontraron datos")
    

@app.post("/api/actualizar_rutaMeli")

async def actualizar_estado(ruta_meli: int, id_ppu : int, fecha: str):
    try:
        conexion = psycopg2.connect(**parametros_conexion)
        cursor = conexion.cursor()
        consulta = f"UPDATE mercadolibre.citacion SET ruta_meli ={ruta_meli} WHERE id_ppu={id_ppu} and fecha='{fecha}'"
        cursor.execute(consulta)
        conexion.commit()
        cursor.close()
        conexion.close()
        print()
        return {"message": "Datos Ingresados Correctamente"}
    except Exception as e: raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/ingresarDriversPeoneta")

async def actualizar_estado(id_driver: int, id_peoneta : int, fecha: str, id_ppu:int):
    try:
        conexion = psycopg2.connect(**parametros_conexion)
        cursor = conexion.cursor()
        consulta = f"UPDATE mercadolibre.citacion SET id_driver ={id_driver}, id_peoneta = {id_peoneta} WHERE fecha='{fecha}' AND id_ppu={id_ppu}"
        cursor.execute(consulta)
        conexion.commit()
        cursor.close()
        conexion.close()
        print()
        return {"message": "Datos Ingresados Correctamente"}
    except Exception as e: raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/patentesPorCitacion")
async def Obtener_datos( op : int, cop : int, fecha: str):
     # Consulta SQL para obtener datos (por ejemplo)
    consulta = f"select * from mercadolibre.recuperar_patentes_citacion({op},{cop},'{fecha}');"
    # Ejecutar la consulta utilizando nuestra función
    datos = ejecutar_consulta(consulta)
    # Verificar si hay datos 
    if datos:
        datos_formateados = [{
                                "id_ppu": fila [0],
                                "ppu": fila[1],
                                "tipo": fila[2],
                                "razon_social": fila [3],
                                "colaborador_id": fila [4],
                                "tripulacion": fila[5]

                            } 
                            for fila in datos]
        return datos_formateados
    else:
        raise HTTPException(status_code=404, detail="No se encontraron datos")

@app.get("/api/filtro/Cop")
async def Obtener_datos( op : int):
     # Consulta SQL para obtener datos (por ejemplo)
    consulta = f"select id, centro from  operacion.centro_operacion co where id_op = {op};"
    # Ejecutar la consulta utilizando nuestra función
    datos = ejecutar_consulta(consulta)
    # Verificar si hay datos 
    if datos:
        datos_formateados = [{
                                "id": fila[0],
                                "centro": fila [1]
                            } 
                            for fila in datos]
        return datos_formateados
    else:
        raise HTTPException(status_code=404, detail="No se encontraron datos")
    
@app.get("/api/filtroPatentesPorIdOp_y_IdCop")
async def Obtener_datos(id_operacion: str, id_centro_op : int):
     # Consulta SQL para obtener datos (por ejemplo)
    consulta = f"select * from mercadolibre.citacion c  where id_operacion = {id_operacion} and id_centro_op = {id_centro_op}"
    # Ejecutar la consulta utilizando nuestra función
    datos = ejecutar_consulta(consulta)
    # Verificar si hay datos 
    if datos:
        datos_formateados = [{  
                                "id": fila[0],
                                "fecha": fila [4],
                                "ruta_meli": fila[5],
                                "id_ppu": fila[6],
                                "id_centro_op": fila[8],
                                "tipo_ruta": fila [9],
                                "id_ppu_amb": fila[10],
                                "ruta_meli_amb": fila[11],
                                "ruta_amb_interna": fila[12],
                                "estado": fila[13]
                                

                            } 
                            for fila in datos]
        return datos_formateados
    else:
        raise HTTPException(status_code=404, detail="No se encontraron datos")


@app.get("/api/tipoRuta")
async def Obtener_datos():
     # Consulta SQL para obtener datos (por ejemplo)
    consulta = f"select * from mercadolibre.tipo_ruta tr "
    # Ejecutar la consulta utilizando nuestra función
    datos = ejecutar_consulta(consulta)
    # Verificar si hay datos 
    if datos:
        datos_formateados = [{  
                                "id": fila[0],
                                "tipo": fila [1]
                            } 
                            for fila in datos]
        return datos_formateados
    else:
        raise HTTPException(status_code=404, detail="No se encontraron datos")
    
@app.post("/api/actualizar_tipoRuta")

async def actualizar_estado(tipo_ruta: int, id_ppu : int, fecha: str):
    try:
        conexion = psycopg2.connect(**parametros_conexion)
        cursor = conexion.cursor()
        consulta = f"UPDATE mercadolibre.citacion SET tipo_ruta ={tipo_ruta} WHERE id_ppu={id_ppu} and fecha='{fecha}'"
        cursor.execute(consulta)
        conexion.commit()
        cursor.close()
        conexion.close()
        print()
        return {"message": "Datos Ingresados Correctamente"}
    except Exception as e: raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/countCitaciones")
async def Obtener_datos(fecha:str, id_cop:int):
     # Consulta SQL para obtener datos (por ejemplo)
    consulta = f"SELECT COUNT(*) FROM mercadolibre.citacion c WHERE c.fecha = '{fecha}'  AND c.id_centro_op ={id_cop} "
    # Ejecutar la consulta utilizando nuestra función
    datos = ejecutar_consulta(consulta)
    # Verificar si hay datos 
    if datos:
        datos_formateados = [{  
                                "ingresados": fila[0]
                            } 
                            for fila in datos]
        return datos_formateados
    else:
        raise HTTPException(status_code=404, detail="No se encontraron datos")


@app.get("/api/countCitacionesConfirmadas")
async def Obtener_datos(fecha:str, id_cop:int, estado: int):
     # Consulta SQL para obtener datos (por ejemplo)
    consulta = f"SELECT COUNT(*) FROM mercadolibre.citacion c WHERE c.fecha = '{fecha}'  AND c.id_centro_op ={id_cop} AND c.estado = {estado}"
    # Ejecutar la consulta utilizando nuestra función
    datos = ejecutar_consulta(consulta)
    # Verificar si hay datos 
    if datos:
        datos_formateados = [{  
                                "ingresados": fila[0]
                            } 
                            for fila in datos]
        return datos_formateados
    else:
        raise HTTPException(status_code=404, detail="No se encontraron datos")

@app.post("/api/Ambulancia")

async def actualizar_estado(id_ppu_amb: int, ruta_meli_amb:str, ruta_amb_interna: str, id_ppu : int, fecha: str):
    try:
        conexion = psycopg2.connect(**parametros_conexion)
        cursor = conexion.cursor()
        consulta = f"UPDATE mercadolibre.citacion SET id_ppu_amb = {id_ppu_amb}, ruta_meli_amb =  '{ruta_meli_amb}', ruta_amb_interna = '{ruta_amb_interna}' WHERE id_ppu={id_ppu} and fecha='{fecha}'"
        cursor.execute(consulta)
        conexion.commit()
        cursor.close()
        conexion.close()
        print()
        return {"message": "Datos Ingresados Correctamente"}
    except Exception as e: raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/AmbulanceCode")
async def Obtener_datos():
     # Consulta SQL para obtener datos (por ejemplo)
    consulta = f"select * from mercadolibre.genera_codigo_ambulancia();"
    # Ejecutar la consulta utilizando nuestra función
    datos = ejecutar_consulta(consulta)
    # Verificar si hay datos 
    if datos:
        datos_formateados = [{
                                "genera_codigo_ambulancia": fila[0],
                            } 
                            for fila in datos]
        return datos_formateados
    else:
        raise HTTPException(status_code=404, detail="No se encontraron datos")
    
@app.post("/api/SaveData")

async def actualizar_estado(ruta_amb_interna: str, id_ppu: int, fecha: str, id_ppu_amb: int, ruta_meli_amb:str):
    try:
        conexion = psycopg2.connect(**parametros_conexion)
        cursor = conexion.cursor()
        consulta = f"UPDATE mercadolibre.citacion SET ruta_amb_interna = '{ruta_amb_interna}', id_ppu_amb = {id_ppu_amb}, ruta_meli_amb = '{ruta_meli_amb}' where id_ppu = {id_ppu} and fecha ='{fecha}'"
        cursor.execute(consulta)
        conexion.commit()
        cursor.close()
        conexion.close()
        print()
        return {"message": "Datos Ingresados Correctamente"}
    except Exception as e: raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/getEstados")
async def Obtener_datos( id_ppu: int, fecha: str):
     # Consulta SQL para obtener datos (por ejemplo)
    consulta = f"select tipo_ruta from mercadolibre.citacion c where fecha ='{fecha}' and id_ppu ='{id_ppu}'"
    # Ejecutar la consulta utilizando nuestra función
    datos = ejecutar_consulta(consulta)
    # Verificar si hay datos 
    if datos:
        datos_formateados = [{
                                "tipo_ruta": fila [0],

                            } 
                            for fila in datos]
        return datos_formateados
    else:
        raise HTTPException(status_code=404, detail="No se encontraron datos")


@app.post("/api/BitacoraGeneral")

async def actualizar_estado(id_usuario: int, ids_usuario:str, modificación: str, latitud : int, longitud: str, origen):
    try:
        conexion = psycopg2.connect(**parametros_conexion)
        cursor = conexion.cursor()
        consulta = f"INSERT INTO mercadolibre.bitacora_general(id_usuario,ids_usuario, modificacion, latitud, longitud, origen)VALUES('1195', 'hela-1195', 'test', '23.3423', '34.4444', 'NO SE QUE ES');"
        cursor.execute(consulta)
        conexion.commit()
        cursor.close()
        conexion.close()
        print()
        return {"message": "Datos Ingresados Correctamente"}
    except Exception as e: raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/infoAMB")
async def Obtener_datos( op: int, cop: int,id_ppu: int, fecha: str):
     # Consulta SQL para obtener datos (por ejemplo)
    consulta = f"select * from mercadolibre.retorno_ambulancia('{fecha}',{op},{cop},{id_ppu});"
    # Ejecutar la consulta utilizando nuestra función
    datos = ejecutar_consulta(consulta)
    # Verificar si hay datos 
    if datos:
        datos_formateados = [{
                                "id_ppu": fila [0],
                                "ppu": fila[1],
                                "ruta_meli": fila[2],

                            } 
                            for fila in datos]
        return datos_formateados
    else:
        raise HTTPException(status_code=404, detail="No se encontraron datos")

if __name__ == "__main__":
 uvicorn.run(app, host="0.0.0.0", port=8000)