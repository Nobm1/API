// Cargar variables de entorno desde el archivo .env
require('dotenv').config();

// Configurar los valores de la base de datos utilizando process.env
const dbConfig = {
    host: process.env.DB_HOST,
    database: process.env.DB_NAME,
    user: process.env.DB_USER,
    password: process.env.DB_PASSWORD,
    port: process.env.DB_PORT
};

// Ejemplo de cómo usar la configuración de la base de datos en tu aplicación
const { Pool } = require('pg');  // Si estás usando PostgreSQL, por ejemplo

// Crear un pool de conexiones utilizando los datos de entorno
const pool = new Pool({
    host: dbConfig.host,
    database: dbConfig.database,
    user: dbConfig.user,
    password: dbConfig.password,
    port: dbConfig.port
});

// Verificar la conexión
pool.connect((err, client, release) => {
    if (err) {
        return console.error('Error al conectar a la base de datos:', err.stack);
    }
    console.log('Conexión exitosa a la base de datos');
    release();  // Liberar el cliente después de la conexión
});

// Ejemplo de una consulta a la base de datos
pool.query('SELECT NOW()', (err, res) => {
    if (err) {
        console.error('Error en la consulta:', err.stack);
    } else {
        console.log('Resultado de la consulta:', res.rows);
    }
    pool.end();  // Cerrar el pool de conexiones después de la consulta
});
