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
class RazonSocial(BaseModel):
    id_user: int
    ids_user: str
    nombre: str
    description: str
    creation_date: str
    update_date: str
    estado: bool 

class updateApp(BaseModel):
    id: int
    estado: bool
# Configurar los orígenes permitidos (permite todas las solicitudes por ahora)
origins = ["*"]

# Agregar middleware CORS a la aplicación
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST","GET","DELETE"],
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
    

@app.post("/Agregar/RazonSocial")
async def Agregar_RazonSocial(body: RazonSocial):
    try:
        conexion = psycopg2.connect(**parametros_conexion)
        cursor = conexion.cursor()
        consulta = f"INSERT INTO operacion.modalidad_operacion(id_user, ids_user, nombre, description, creation_date, update_date, estado ) VALUES ({body.id_user}, '{body.ids_user}','{body.nombre}', '{body.description}','{body.creation_date}','{body.update_date}',{body.estado})"
        cursor.execute(consulta, (body.id_user,body.ids_user,body.nombre, body.description, body.creation_date, body.update_date, body.estado))
        conexion.commit()
        cursor.close()
        conexion.close()
        print()
        return {"message": "Datos Ingresados Correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/Api/Modalidad")
async def Obtener_datos():
     # Consulta SQL para obtener datos (por ejemplo)
    consulta = "select * from operacion.modalidad_operacion mo"
    # Ejecutar la consulta utilizando nuestra función
    datos = ejecutar_consulta(consulta)
    # Verificar si hay datos
    if datos:
        datos_formateados = [{
                                "id" : fila[0],
                                "created_at": fila[1],
                                "id_user": fila [2],
                                "ids:user": fila[3],
                                "nombre" : fila[4],
                                "description" : fila[5],
                                "Creation_date" : fila[6],
                                "update_date": fila[7],
                                "estado" : fila[8]
                            } 
                            for fila in datos]
        return datos_formateados
    else:
        raise HTTPException(status_code=404, detail="No se encontraron datos")


@app.get("/Api/Modalidad/Buscar")
async def Obtener_datos(nombre: str):
     # Consulta SQL para obtener datos (por ejemplo)
    consulta = f"select * from operacion.modalidad_operacion mo  where nombre = '{nombre}'"
    # Ejecutar la consulta utilizando nuestra función
    datos = ejecutar_consulta(consulta)
    # Verificar si hay datos
    if datos:
        datos_formateados = [{
                                "id" : fila[0],
                                "created_at": fila[1],
                                "id_user": fila [2],
                                "ids:user": fila[3],
                                "nombre" : fila[4],
                                "description" : fila[5],
                                "Creation_date" : fila[6],
                                "update_date": fila[7],
                                "estado" : fila[8]
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

@app.delete("/Modalidad/borrar")
async def eliminar_modalidad(id: str):
    # Construir la sentencia SQL de eliminación
    sql = f"DELETE FROM operacion.modalidad_operacion WHERE id = {id};"
    # Llamar a la función para ejecutar la sentencia SQL de eliminación
    ejecutar_delete(sql)
    return {"message": f"Entrada con ID {id} eliminada correctamente"}


@app.post("/actualizar_estado")
async def actualizar_estado(ud: updateApp):
    try:
        conexion = psycopg2.connect(**parametros_conexion)
        cursor = conexion.cursor()
        consulta = f"UPDATE operacion.modalidad_operacion SET estado={ud.estado} WHERE id={ud.id}"
        cursor.execute(consulta, (ud.estado, ud.id))
        conexion.commit()
        cursor.close()
        conexion.close()
        print()
        return {"message": "Datos Ingresados Correctamente"}
    except Exception as e: raise HTTPException(status_code=500, detail=str(e))

# # Función para actualizar el estado en la base de datos
# @app.patch("/actualizar_estado/")
# async def actualizar_estado(item_id: int, estado: bool):
#     try:
#         # Conexión a la base de datos PostgreSQL
#         conexion = psycopg2.connect(**parametros_conexion)
#         cursor = conexion.cursor()
#         # Consulta SQL para actualizar el estado
#         consulta = f"UPDATE operacion.modalidad_operacion SET estado={estado} WHERE id={item_id}"
#         cursor.execute(consulta)
#         conexion.commit()
#         cursor.close()
#         conexion.close()
#         return {"message": "Datos actualizados correctamente"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
    

if __name__ == "__main__":
 uvicorn.run(app, host="0.0.0.0", port=8000)

