from fastapi import APIRouter, Request, Depends, HTTPException, Header
from app.database import get_connection
from app.services.export_service import export_data
from app.services.stats_service import registrar_uso
from datetime import timedelta
from typing import Optional

router = APIRouter(prefix="/api")

@router.get("/eventos")
def eventos(
    request: Request, 
    formato: str = "json", 
    download: bool = False, 
    consume: bool = False,
    api_key: Optional[str] = None,
    x_api_key: Optional[str] = Header(None)
):
    
    # Validar API Key (por query o por header)
    key_to_check = api_key or x_api_key
    if not key_to_check:
        raise HTTPException(status_code=401, detail="API Key es requerida. Envía 'api_key' como query parameter o 'X-API-Key' en los headers.")
        
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Checar si la llave es válida
    cursor.execute("SELECT username FROM usuarios WHERE api_key=%s", (key_to_check,))
    user_data = cursor.fetchone()
    
    if not user_data:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=401, detail="API Key inválida.")
        
    api_username = user_data["username"]

    cursor.execute("SELECT * FROM eventos")
    data = cursor.fetchall()
    

    cursor.close()
    conn.close()
    
    import datetime
    import decimal
    for index, row in enumerate(data):
        if 'hora' in row and isinstance(row['hora'], timedelta):
            row['hora'] = str(row['hora'])
        if 'fecha' in row and isinstance(row['fecha'], datetime.date):
            row['fecha'] = str(row['fecha'])
        if 'precio' in row and isinstance(row['precio'], decimal.Decimal):
            row['precio'] = float(row['precio'])

    ip = request.client.host
    registrar_uso("/api/eventos", formato, ip, api_username)

    return export_data(data, formato, download)


@router.get("/stats")
def stats():

    conn=get_connection()

    cursor=conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM api_stats ORDER BY fecha DESC")

    data=cursor.fetchall()

    cursor.close()
    conn.close()

    return data