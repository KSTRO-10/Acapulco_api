from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.database import get_connection

router = APIRouter(prefix="/admin")
templates = Jinja2Templates(directory="app/templates")

# Helper para checar sesión de admin
def check_admin_session(request: Request):
    user = request.session.get("user")
    rol = request.session.get("rol")
    if not user or rol != "admin":
        return False
    return True

@router.get("/", response_class=HTMLResponse, name="admin_dashboard")
def admin_dashboard(request: Request):
    # Proteger ruta para ADMIN
    if not check_admin_session(request):
        return RedirectResponse(url="/login", status_code=303)
        
    # Obtener estadísticas de uso de la API
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM api_stats ORDER BY fecha DESC LIMIT 50")
    stats = cursor.fetchall()
    
    # Formatear la fecha para que se vea más limpia
    for stat in stats:
        if stat["fecha"]:
            stat["fecha"] = stat["fecha"].strftime("%Y-%m-%d %H:%M:%S")
            
    # Obtener eventos
    cursor.execute("SELECT * FROM eventos ORDER BY fecha DESC")
    eventos = cursor.fetchall()

    # Obtener api_key del admin para el visor JSON
    username = request.session.get("user")
    cursor.execute("SELECT api_key FROM usuarios WHERE username=%s", (username,))
    user_row = cursor.fetchone()
    api_key = user_row["api_key"] if user_row else ""
            
    cursor.close()
    conn.close()

    return templates.TemplateResponse(
        "admin.html",
        {
            "request": request,
            "stats": stats,
            "eventos": eventos,
            "api_key": api_key
        }
    )

@router.post("/evento", name="crear_evento")
def crear_evento(
    request: Request,
    nombre: str = Form(...),
    descripcion: str = Form(...),
    lugar: str = Form(...),
    hora: str = Form(...),
    fecha: str = Form(...),
    imagen_url: str = Form(None),
    categoria: str = Form("General"),
    precio: float = Form(0.0)
):
    # Proteger ruta
    if not check_admin_session(request):
        return RedirectResponse(url="/login", status_code=303)

    conn = get_connection()
    cursor = conn.cursor()

    sql = """
    INSERT INTO eventos(nombre,descripcion,lugar,hora,fecha, imagen_url, categoria, precio)
    VALUES(%s,%s,%s,%s,%s,%s,%s,%s)
    """

    cursor.execute(sql, (nombre, descripcion, lugar, hora, fecha, imagen_url, categoria, precio))
    conn.commit()

    cursor.close()
    conn.close()

    # Redirigir de vuelta al panel con mensaje de éxito (pasado por sesión o query param, en este caso renderizamos directo)
    # Para mantener las estadísticas, volvemos a hacer el query
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM api_stats ORDER BY fecha DESC LIMIT 50")
    stats = cursor.fetchall()
    for stat in stats:
        if stat["fecha"]:
            stat["fecha"] = stat["fecha"].strftime("%Y-%m-%d %H:%M:%S")
    cursor.close()
    conn.close()

    # Traer todos los eventos de nuevo
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM eventos ORDER BY fecha DESC")
    eventos = cursor.fetchall()
    cursor.close()
    conn.close()

    return templates.TemplateResponse(
        "admin.html",
        {
            "request": request, 
            "stats": stats,
            "eventos": eventos,
            "mensaje": "¡Evento creado con éxito!"
        }
    )

@router.post("/evento/eliminar", name="eliminar_evento")
def eliminar_evento(request: Request, evento_id: int = Form(...)):
    if not check_admin_session(request):
        return RedirectResponse(url="/login", status_code=303)
        
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM eventos WHERE id=%s", (evento_id,))
    conn.commit()
    cursor.close()
    conn.close()
    
    return RedirectResponse(url="/admin", status_code=303)

@router.post("/evento/editar", name="editar_evento")
def editar_evento(
    request: Request,
    evento_id: int = Form(...),
    nombre: str = Form(...),
    descripcion: str = Form(...),
    lugar: str = Form(...),
    hora: str = Form(...),
    fecha: str = Form(...),
    imagen_url: str = Form(None),
    categoria: str = Form("General"),
    precio: float = Form(0.0)
):
    if not check_admin_session(request):
        return RedirectResponse(url="/login", status_code=303)
        
    conn = get_connection()
    cursor = conn.cursor()
    
    sql = """
    UPDATE eventos 
    SET nombre=%s, descripcion=%s, lugar=%s, hora=%s, fecha=%s, imagen_url=%s, categoria=%s, precio=%s 
    WHERE id=%s
    """
    cursor.execute(sql, (nombre, descripcion, lugar, hora, fecha, imagen_url, categoria, precio, evento_id))
    conn.commit()
    cursor.close()
    conn.close()
    
    return RedirectResponse(url="/admin", status_code=303)