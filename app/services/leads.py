from app.services.database import get_connection


def guardar_cliente(sender_id, nombre=None, telefono=None):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO clientes (sender_id, nombre, telefono)
        VALUES (%s, %s, %s)
        ON CONFLICT (sender_id)
        DO UPDATE SET
            nombre = COALESCE(EXCLUDED.nombre, clientes.nombre),
            telefono = COALESCE(EXCLUDED.telefono, clientes.telefono);
    """, (sender_id, nombre, telefono))

    conn.commit()
    cur.close()
    conn.close()


def guardar_conversacion(sender_id, mensaje_usuario, respuesta_bot):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO conversaciones (sender_id, mensaje_usuario, respuesta_bot)
        VALUES (%s, %s, %s);
    """, (sender_id, mensaje_usuario, respuesta_bot))

    conn.commit()
    cur.close()
    conn.close()


def guardar_oportunidad(sender_id, vehiculo_consultado=None, interes=None):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO oportunidades (sender_id, vehiculo_consultado, interes)
        VALUES (%s, %s, %s);
    """, (sender_id, vehiculo_consultado, interes))

    conn.commit()
    cur.close()
    conn.close()
    
    
    # Esto guarda todo lo que se converso , cliente y la oportunidad de venta . Es para tener los datos actualizados 
    