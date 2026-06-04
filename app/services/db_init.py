from app.services.database import get_connection


def crear_tablas():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id SERIAL PRIMARY KEY,
            sender_id TEXT UNIQUE NOT NULL,
            nombre TEXT,
            telefono TEXT,
            origen TEXT DEFAULT 'messenger',
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS conversaciones (
            id SERIAL PRIMARY KEY,
            sender_id TEXT NOT NULL,
            mensaje_usuario TEXT,
            respuesta_bot TEXT,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS oportunidades (
            id SERIAL PRIMARY KEY,
            sender_id TEXT NOT NULL,
            vehiculo_consultado TEXT,
            interes TEXT,
            estado TEXT DEFAULT 'nuevo',
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    conn.commit()
    cur.close()
    conn.close()

    print("Tablas creadas correctamente ✅")
    
    
    #Esto guarda los datos de los clientes. 
    