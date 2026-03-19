import os
import sys

# Añadir el directorio raíz al path para importar app.database
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.database import get_connection

def populate_events():
    eventos = [
        {
            "nombre": "Festival Francés de Acapulco",
            "descripcion": "Una celebración de la cultura, cine y gastronomía francesa en el corazón de Acapulco.",
            "lugar": "Centro de Convenciones Acapulco",
            "hora": "18:00:00",
            "fecha": "2026-04-15",
            "imagen_url": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?auto=format&fit=crop&q=80&w=1000",
            "categoria": "Cultura",
            "precio": 250.0
        },
        {
            "nombre": "Abierto Mexicano de Tenis",
            "descripcion": "El torneo de tenis más importante de México con las estrellas del ATP.",
            "lugar": "Arena GNP Seguros",
            "hora": "16:00:00",
            "fecha": "2026-03-25",
            "imagen_url": "https://images.unsplash.com/photo-1592709823125-a191f07a2a5e?auto=format&fit=crop&q=80&w=1000",
            "categoria": "Deporte",
            "precio": 1500.0
        },
        {
            "nombre": "Show de Clavadistas La Quebrada",
            "descripcion": "Espectáculo nocturno con antorchas de los valientes clavadistas.",
            "lugar": "La Quebrada, Acapulco Tradicional",
            "hora": "20:30:00",
            "fecha": "2026-03-20",
            "imagen_url": "https://images.unsplash.com/photo-1533038590840-1cde6e668a91?auto=format&fit=crop&q=80&w=1000",
            "categoria": "Turismo",
            "precio": 100.0
        },
        {
            "nombre": "Sunset Party Pie de la Cuesta",
            "descripcion": "Disfruta del mejor atardecer con música en vivo y cócteles.",
            "lugar": "Playa Pie de la Cuesta",
            "hora": "17:30:00",
            "fecha": "2026-03-21",
            "imagen_url": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&q=80&w=1000",
            "categoria": "Entretenimiento",
            "precio": 0.0
        },
        {
            "nombre": "Recorrido Yate Bonanza",
            "descripcion": "Tour por la bahía de Santa Lucía con barra libre y animación.",
            "lugar": "Muelle Paseo del Pescador",
            "hora": "16:30:00",
            "fecha": "2026-03-22",
            "imagen_url": "https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?auto=format&fit=crop&q=80&w=1000",
            "categoria": "Turismo",
            "precio": 450.0
        },
        {
            "nombre": "Feria Imperial Acapulco",
            "descripcion": "Juegos mecánicos, conciertos y exposiciones para toda la familia.",
            "lugar": "Mundo Imperial, Zona Diamante",
            "hora": "15:00:00",
            "fecha": "2026-12-28",
            "imagen_url": "https://images.unsplash.com/photo-1528605248644-14dd04cb220d?auto=format&fit=crop&q=80&w=1000",
            "categoria": "Entretenimiento",
            "precio": 150.0
        },
        {
            "nombre": "Avistamiento de Ballenas",
            "descripcion": "Tour guiado para observar ballenas jorobadas en la costa de Guerrero.",
            "lugar": "Puerto Marqués",
            "hora": "08:00:00",
            "fecha": "2026-03-18",
            "imagen_url": "https://images.unsplash.com/photo-1522271897361-55822363b93f?auto=format&fit=crop&q=80&w=1000",
            "categoria": "Naturaleza",
            "precio": 800.0
        },
        {
            "nombre": "Torneo de Surf Revolcadero",
            "descripcion": "Los mejores surfistas locales compiten en las olas de Playa Revolcadero.",
            "lugar": "Playa Revolcadero",
            "hora": "07:00:00",
            "fecha": "2026-05-10",
            "imagen_url": "https://images.unsplash.com/photo-1502680390469-be75c86b636f?auto=format&fit=crop&q=80&w=1000",
            "categoria": "Deporte",
            "precio": 0.0
        },
        {
            "nombre": "Noche de Gala Fuerte de San Diego",
            "descripcion": "Recorrido nocturno teatralizado por la emblemática fortaleza.",
            "lugar": "Museo Histórico de Acapulco Fuerte de San Diego",
            "hora": "19:00:00",
            "fecha": "2026-04-02",
            "imagen_url": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?auto=format&fit=crop&q=80&w=1000",
            "categoria": "Historia",
            "precio": 200.0
        },
        {
            "nombre": "Carnaval de Acapulco",
            "descripcion": "Desfiles alegóricos, música y baile a lo largo de la Costera Miguel Alemán.",
            "lugar": "Costera Miguel Alemán",
            "hora": "17:00:00",
            "fecha": "2026-02-15",
            "imagen_url": "https://images.unsplash.com/photo-1527871369852-eb58cb2b59f2?auto=format&fit=crop&q=80&w=1000",
            "categoria": "Cultura",
            "precio": 0.0
        }
    ]

    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        sql = """
        INSERT INTO eventos (nombre, descripcion, lugar, hora, fecha, imagen_url, categoria, precio)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        data = [
            (e["nombre"], e["descripcion"], e["lugar"], e["hora"], e["fecha"], e["imagen_url"], e["categoria"], e["precio"])
            for e in eventos
        ]
        
        cursor.executemany(sql, data)
        conn.commit()
        
        print(f"Successfully inserted {cursor.rowcount} events.")
        
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        print("\nMake sure you have the correct credentials in your .env file or environment variables.")
        print("Required variables: DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME")

if __name__ == "__main__":
    populate_events()
