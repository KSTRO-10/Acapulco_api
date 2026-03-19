<<<<<<< HEAD
=======
import os
>>>>>>> 19ed2aa1da0a602905dbb3b1c2428029cbb1907d
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

from app.routers import api_routes
from app.routers import admin_routes

app = FastAPI(title="API Turismo Acapulco")

# Añadir middleware de sesión
app.add_middleware(SessionMiddleware, secret_key="super_secret_key_acapulco")

<<<<<<< HEAD
app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")
=======
# Rutas absolutas para evitar errores 500 en Vercel
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))
>>>>>>> 19ed2aa1da0a602905dbb3b1c2428029cbb1907d

from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi import Form
from app.database import get_connection

@app.get("/")
def home(request: Request):
    user = request.session.get("user")
    rol = request.session.get("rol")
    
    # Si hay sesión, redirigimos a donde toque
    if user:
        if rol == "admin":
            return RedirectResponse(url="/admin", status_code=303)
        else:
            return RedirectResponse(url="/eventos", status_code=303)
            
    # Si no hay sesión, al login
    return RedirectResponse(url="/login", status_code=303)

@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    user = request.session.get("user")
    if user:
        return RedirectResponse(url="/", status_code=303)
        
    return templates.TemplateResponse(
        "login.html",
        {"request": request}
    )

@app.post("/login")
def login_post(request: Request, username: str = Form(...), password: str = Form(...)):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Validar usuario y obtener rol
    cursor.execute("SELECT * FROM usuarios WHERE username=%s AND password=%s", (username, password))
    user = cursor.fetchone()
    
    if user:
        # Generar API Key si es un usuario antiguo que no la tiene
        if not user.get("api_key"):
            import secrets
            api_key_str = secrets.token_hex(16)
            cursor.execute("UPDATE usuarios SET api_key=%s WHERE username=%s", (api_key_str, username))
            conn.commit()
            user["api_key"] = api_key_str
            
        cursor.close()
        conn.close()
        
        request.session["user"] = user["username"]
        request.session["rol"] = user.get("rol", "consumidor") # Guardar el rol en sesión
        return RedirectResponse(url="/", status_code=303)
    else:
        cursor.close()
        conn.close()
        
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Credenciales inválidas"}
        )

@app.get("/registro", response_class=HTMLResponse)
def registro_page(request: Request):
    user = request.session.get("user")
    if user:
        return RedirectResponse(url="/", status_code=303)
        
    return templates.TemplateResponse(
        "registro.html",
        {"request": request}
    )

@app.post("/registro")
def registro_post(request: Request, username: str = Form(...), password: str = Form(...)):
    import secrets
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Verificar si existe el usuario
    cursor.execute("SELECT * FROM usuarios WHERE username=%s", (username,))
    existing_user = cursor.fetchone()
    
    if existing_user:
        cursor.close()
        conn.close()
        return templates.TemplateResponse(
            "registro.html",
            {"request": request, "error": "El usuario ya existe. Intenta con otro nombre."}
        )
    
    # Generar API Key
    api_key_str = secrets.token_hex(16)
    
    # Crear usuario
    cursor.execute("INSERT INTO usuarios (username, password, rol, api_key) VALUES (%s, %s, %s, %s)", (username, password, "consumidor", api_key_str))
    conn.commit()
    
    cursor.close()
    conn.close()
    
    # Auto-login
    request.session["user"] = username
    request.session["rol"] = "consumidor"
    return RedirectResponse(url="/eventos", status_code=303)

@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login", status_code=303)

@app.get("/eventos")
def vista_eventos(request: Request):
    # Proteger vista solo para logueados (pueden ser consumidor o admin)
    user = request.session.get("user")
    if not user:
        return RedirectResponse(url="/login", status_code=303)
        
    # Obtener API Key
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT api_key FROM usuarios WHERE username=%s", (user,))
    db_user = cursor.fetchone()
    cursor.close()
    conn.close()
    
    api_key = db_user["api_key"] if db_user else None

    return templates.TemplateResponse(
        "index.html",
        {"request": request, "user": user, "rol": request.session.get("rol"), "api_key": api_key}
    )



app.include_router(api_routes.router)
app.include_router(admin_routes.router)