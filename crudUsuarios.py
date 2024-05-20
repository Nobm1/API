from fastapi import FastAPI,HTTPException
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
from pydantic import BaseModel

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
class usuario(BaseModel):
    created_at: str
    id_ingreso_hela: int 
    id_user: int
    ids_user: str
    id_razon_social: int 
    jpg_foto_perfil: str
    nombre_completo: str
    rut: str
    nroseriecedula: str 
    email: str
    telefono: str       
    birthday: str
    region: str
    comuna: str
    domicilio: str
    tipo_usuario: int 
    pdf_antecedentes: str 
    pdf_licencia_conducir: str 
    fec_venc_lic_conducir: str
    pdf_cedula_identidad: str
    pdf_contrato: str
    activo: bool
    validacion_seguridad: int 
    validacion_transporte: int

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
    
@app.post("/usuario/agregar")
async def usuario_agregar(body: usuario):
    try:
        conexion = psycopg2.connect(**parametros_conexion)
        cursor = conexion.cursor()
        consulta = f"INSERT INTO transporte.usuarios (
                                        created_at,
                                        id_ingreso_hela, 
                                        id_user, 
                                        ids_user, 
                                        id_razon_social, 
                                        jpg_foto_perfil, 
                                        nombre_completo, 
                                        rut, 
                                        nroseriecedula, 
                                        email, 
                                        telefono, 
                                        birthday, 
                                        region, 
                                        comuna, 
                                        domicilio, 
                                        tipo_usuario, 
                                        pdf_antecedentes, 
                                        pdf_licencia_conducir, 
                                        fec_venc_lic_conducir, 
                                        pdf_cedula_identidad, 
                                        pdf_contrato, activo, 
                                        validacion_seguridad, 
                                        validacion_transporte) 
                                        
                    VALUES (             {body.id},
                                        {body.created_at},
                                        {body.id_ingreso_hela}, 
                                        {body.id_user}, 
                                        {body.ids_user}, 
                                        {body.id_razon_social}, 
                                        {body.jpg_foto_perfil}, 
                                        {body.nombre_completo}, 
                                        {body.rut}, 
                                        {body.nroseriecedula}, 
                                        {body.email}, 
                                        {body.telefono}, 
                                        {body.birthday}, 
                                        {body.region}, 
                                        {body.comuna}, 
                                        {body.domicilio}, 
                                        {body.tipo_usuario}, 
                                        {body.pdf_antecedentes}, 
                                        {body.pdf_licencia_conducir}, 
                                        {body.fec_venc_lic_conducir}, 
                                        {body.pdf_cedula_identidad}, 
                                        {body.pdf_contrato},
                                        {body.activo}, 
                                        {body.validacion_seguridad}, 
                                        {body.validacion_transporte});"
        cursor.execute(consulta,(   
                                        body.created_at,
                                        body.id_ingreso_hela, 
                                        body.id_user, 
                                        body.ids_user, 
                                        body.id_razon_social, 
                                        body.jpg_foto_perfil, 
                                        body.nombre_completo, 
                                        body.rut, body.
                                        body.nroseriecedula, 
                                        body.email, 
                                        body.telefono, 
                                        body.birthday, 
                                        body.region, 
                                        body.comuna, 
                                        body.domicilio, 
                                        body.tipo_usuario, 
                                        body.pdf_antecedentes, 
                                        body.pdf_licencia_conducir, 
                                        body.fec_venc_lic_conducir, 
                                        body.pdf_cedula_identidad, 
                                        body.pdf_contrato, 
                                        body.activo, 
                                        body.validacion_seguridad, 
                                        body.validacion_transporte))
        conexion.commit()
        cursor.close()
        conexion.close()
        print()
        return {"message": "Datos Ingresados Correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))