# ANÁLISIS DE PUNTOS DE FUNCIÓN — PROYECTO "ACAPULCO API"
## (Catálogo Emprendedor Digital / API Turismo Acapulco)

**Fecha:** 12 de Marzo de 2026  
**Proyecto:** Acapulco API — Sistema de Turismo con Web Service RESTful  
**Tecnologías:** Python · FastAPI · MySQL (Aiven Cloud) · Jinja2 · Vercel  

---

## 1. IDENTIFICACIÓN DE FUNCIONES TRANSACCIONALES Y DE DATOS

### 1.1 Archivos Lógicos Internos (ILF – Internal Logical Files)

Son los grupos de datos mantenidos por la propia aplicación.

| ID  | ILF                | Descripción                                    |
|-----|--------------------|-------------------------------------------------|
| ILF-1 | **Usuarios**     | Tabla `usuarios` — almacena credenciales, roles y API Keys |
| ILF-2 | **Eventos**      | Tabla `eventos` — almacena los eventos turísticos/culturales |
| ILF-3 | **API Stats**    | Tabla `api_stats` — registra cada consumo de la API REST |

### 1.2 Archivos de Interfaz Externa (EIF – External Interface Files)

Son datos referenciados/leídos pero mantenidos por otro sistema.

| ID  | EIF                       | Descripción                                                     |
|-----|---------------------------|-----------------------------------------------------------------|
| EIF-1 | **Servicio de Imágenes Externas** | URLs de imágenes almacenadas en servidores externos (placehold.co, etc.) referenciadas en los eventos |

### 1.3 Entradas Externas (EI – External Inputs)

Procesos que ingresan o modifican datos en la aplicación.

| ID   | EI                         | Descripción                                              |
|------|----------------------------|----------------------------------------------------------|
| EI-1 | **Login de usuario**       | Formulario POST `/login` — valida credenciales contra `usuarios` y genera API Key si no existe |
| EI-2 | **Registro de usuario**    | Formulario POST `/registro` — inserta nuevo usuario con rol "consumidor" y API Key |
| EI-3 | **Crear evento**           | Formulario POST `/admin/evento` — inserta evento nuevo en tabla `eventos` |
| EI-4 | **Editar evento**          | Formulario POST `/admin/evento/editar` — actualiza un evento existente |
| EI-5 | **Eliminar evento**        | Formulario POST `/admin/evento/eliminar` — borra un evento por ID |
| EI-6 | **Logout**                 | GET `/logout` — limpia la sesión del usuario |

### 1.4 Salidas Externas (EO – External Outputs)

Procesos que envían datos procesados/calculados fuera del sistema.

| ID   | EO                            | Descripción                                                     |
|------|-------------------------------|-----------------------------------------------------------------|
| EO-1 | **API REST Eventos (JSON)**   | GET `/api/eventos?formato=json` — retorna datos de eventos en JSON + registra estadística de uso |
| EO-2 | **API REST Eventos (XML)**    | GET `/api/eventos?formato=xml` — retorna datos convertidos a XML + registra estadística |
| EO-3 | **API REST Eventos (TXT)**    | GET `/api/eventos?formato=txt` — retorna datos en texto plano + registra estadística |
| EO-4 | **Exportar/Descargar eventos**| GET `/api/eventos?download=true` — genera archivo descargable (JSON/XML/TXT) |

### 1.5 Consultas Externas (EQ – External Queries)

Procesos que recuperan datos sin modificarlos ni realizar procesamiento derivado.

| ID   | EQ                                  | Descripción                                             |
|------|--------------------------------------|---------------------------------------------------------|
| EQ-1 | **Página de Login**                  | GET `/login` — muestra formulario (consulta sesión)     |
| EQ-2 | **Página de Registro**               | GET `/registro` — muestra formulario (consulta sesión)  |
| EQ-3 | **Vista de Eventos (consumidor)**    | GET `/eventos` — muestra catálogo de eventos al usuario logueado |
| EQ-4 | **Dashboard Admin**                  | GET `/admin` — muestra estadísticas de API + lista de eventos |
| EQ-5 | **API Stats**                        | GET `/api/stats` — retorna historial de consumo de la API |
| EQ-6 | **Redirección Home**                 | GET `/` — verifica sesión y redirige según rol |

---

## 2. CONTEO DE DET (Data Element Types)

### 2.1 DETs por ILF

#### ILF-1: Usuarios

| #  | DET (Campo)     | Tipo en BD        |
|----|-----------------|-------------------|
| 1  | id              | INT AUTO_INCREMENT|
| 2  | username        | VARCHAR(50)       |
| 3  | password        | VARCHAR(255)      |
| 4  | rol             | VARCHAR(20)       |
| 5  | api_key         | VARCHAR(100)      |

**Total DET = 5**

#### ILF-2: Eventos

| #  | DET (Campo)     | Tipo en BD        |
|----|-----------------|-------------------|
| 1  | id              | INT AUTO_INCREMENT|
| 2  | nombre          | VARCHAR(150)      |
| 3  | descripcion     | TEXT              |
| 4  | lugar           | VARCHAR(150)      |
| 5  | hora            | TIME              |
| 6  | fecha           | DATE              |
| 7  | imagen_url      | VARCHAR (URL)     |
| 8  | categoria       | VARCHAR           |
| 9  | precio          | DECIMAL           |

**Total DET = 9**

#### ILF-3: API Stats

| #  | DET (Campo)     | Tipo en BD          |
|----|-----------------|---------------------|
| 1  | id              | INT AUTO_INCREMENT  |
| 2  | endpoint        | VARCHAR(100)        |
| 3  | formato         | VARCHAR(20)         |
| 4  | ip              | VARCHAR(50)         |
| 5  | username        | VARCHAR(50)         |
| 6  | fecha           | TIMESTAMP           |

**Total DET = 6**

### 2.2 DETs por EIF

#### EIF-1: Servicio de Imágenes Externas

| #  | DET (Campo)     | Descripción              |
|----|-----------------|--------------------------|
| 1  | imagen_url      | URL de la imagen externa |

**Total DET = 1**

### 2.3 DETs por Entradas Externas (EI)

| ID   | Función                 | DETs (campos visibles para el usuario)                                                    | Total DET |
|------|-------------------------|-------------------------------------------------------------------------------------------|-----------|
| EI-1 | Login                   | username, password, mensaje_error                                                         | 3         |
| EI-2 | Registro                | username, password, mensaje_error                                                         | 3         |
| EI-3 | Crear Evento            | nombre, descripcion, lugar, hora, fecha, imagen_url, categoria, precio, mensaje_éxito      | 9         |
| EI-4 | Editar Evento           | evento_id, nombre, descripcion, lugar, hora, fecha, imagen_url, categoria, precio          | 9         |
| EI-5 | Eliminar Evento         | evento_id, confirmación                                                                    | 2         |
| EI-6 | Logout                  | acción (limpiar sesión)                                                                    | 1         |

### 2.4 DETs por Salidas/Consultas Externas (EO/EQ)

| ID   | Función                    | DETs                                                                                           | Total DET |
|------|----------------------------|------------------------------------------------------------------------------------------------|-----------|
| EO-1 | API Eventos JSON           | id, nombre, descripcion, lugar, hora, fecha, imagen_url, categoria, precio + api_key validada  | 10        |
| EO-2 | API Eventos XML            | id, nombre, descripcion, lugar, hora, fecha, imagen_url, categoria, precio + api_key validada  | 10        |
| EO-3 | API Eventos TXT            | id, nombre, descripcion, lugar, hora, fecha, imagen_url, categoria, precio + api_key validada  | 10        |
| EO-4 | Descargar Eventos          | id, nombre, descripcion, lugar, hora, fecha, imagen_url, categoria, precio + formato + api_key | 11        |
| EQ-1 | Página Login               | username, password                                                                             | 2         |
| EQ-2 | Página Registro            | username, password                                                                             | 2         |
| EQ-3 | Vista Eventos (consumidor) | user, rol, api_key + datos de eventos (nombre, descripcion, lugar, hora, fecha, imagen, cat, precio) | 11        |
| EQ-4 | Dashboard Admin            | stats(username, endpoint, formato, ip, fecha) + eventos(nombre, lugar, fecha, hora) + mensaje  | 11        |
| EQ-5 | API Stats                  | id, endpoint, formato, ip, username, fecha                                                     | 6         |
| EQ-6 | Redirección Home           | user, rol                                                                                      | 2         |

---

## 3. CONTEO DE FTR (File Types Referenced) Y RET (Record Element Types)

### 3.1 RET por cada ILF/EIF (Record Element Types)

Los RET representan subgrupos de datos reconocibles dentro de un archivo lógico.

| Archivo Lógico | RET                        | Cantidad RET |
|----------------|----------------------------|--------------|
| ILF-1: Usuarios | Un solo tipo de registro (usuario) | 1           |
| ILF-2: Eventos  | Un solo tipo de registro (evento)  | 1           |
| ILF-3: API Stats | Un solo tipo de registro (stat)   | 1           |
| EIF-1: Imágenes Externas | Un tipo (URL imagen)     | 1           |

### 3.2 FTR por cada EI/EO/EQ (File Types Referenced)

Los FTR son los archivos lógicos (ILF/EIF) que cada transacción lee o modifica.

| ID   | Función                    | FTR referenciados                              | Total FTR |
|------|----------------------------|-------------------------------------------------|-----------|
| EI-1 | Login                      | ILF-1 (Usuarios)                                | 1         |
| EI-2 | Registro                   | ILF-1 (Usuarios)                                | 1         |
| EI-3 | Crear Evento               | ILF-2 (Eventos)                                 | 1         |
| EI-4 | Editar Evento              | ILF-2 (Eventos)                                 | 1         |
| EI-5 | Eliminar Evento            | ILF-2 (Eventos)                                 | 1         |
| EI-6 | Logout                     | ILF-1 (Usuarios — sesión)                       | 1         |
| EO-1 | API Eventos JSON           | ILF-2 (Eventos), ILF-1 (Usuarios), ILF-3 (Stats) | 3       |
| EO-2 | API Eventos XML            | ILF-2 (Eventos), ILF-1 (Usuarios), ILF-3 (Stats) | 3       |
| EO-3 | API Eventos TXT            | ILF-2 (Eventos), ILF-1 (Usuarios), ILF-3 (Stats) | 3       |
| EO-4 | Descargar Eventos          | ILF-2 (Eventos), ILF-1 (Usuarios), ILF-3 (Stats) | 3       |
| EQ-1 | Página Login               | (Ninguno — vista estática)                       | 0         |
| EQ-2 | Página Registro            | (Ninguno — vista estática)                       | 0         |
| EQ-3 | Vista Eventos (consumidor) | ILF-1 (Usuarios), ILF-2 (Eventos)               | 2         |
| EQ-4 | Dashboard Admin            | ILF-3 (API Stats), ILF-2 (Eventos)              | 2         |
| EQ-5 | API Stats                  | ILF-3 (API Stats)                                | 1         |
| EQ-6 | Redirección Home           | ILF-1 (Usuarios — sesión)                        | 1         |

---

## 4. CÁLCULO DE COMPLEJIDAD Y PUNTOS DE FUNCIÓN SIN AJUSTAR (PFSA)

### 4.1 Matriz de Complejidad IFPUG

#### Para ILF (Internal Logical Files):

| RET \ DET         | 1–19 DET | 20–50 DET | 51+ DET |
|--------------------|----------|-----------|---------|
| **1 RET**          | Baja     | Baja      | Media   |
| **2–5 RET**        | Baja     | Media     | Alta    |
| **6+ RET**         | Media    | Alta      | Alta    |

#### Para EIF (External Interface Files):

| RET \ DET         | 1–19 DET | 20–50 DET | 51+ DET |
|--------------------|----------|-----------|---------|
| **1 RET**          | Baja     | Baja      | Media   |
| **2–5 RET**        | Baja     | Media     | Alta    |
| **6+ RET**         | Media    | Alta      | Alta    |

#### Para EI (External Inputs):

| FTR \ DET         | 1–4 DET  | 5–15 DET  | 16+ DET |
|--------------------|----------|-----------|---------|
| **0–1 FTR**        | Baja     | Baja      | Media   |
| **2 FTR**          | Baja     | Media     | Alta    |
| **3+ FTR**         | Media    | Alta      | Alta    |

#### Para EO (External Outputs):

| FTR \ DET         | 1–5 DET  | 6–19 DET  | 20+ DET |
|--------------------|----------|-----------|---------|
| **0–1 FTR**        | Baja     | Baja      | Media   |
| **2–3 FTR**        | Baja     | Media     | Alta    |
| **4+ FTR**         | Media    | Alta      | Alta    |

#### Para EQ (External Queries):

| FTR \ DET         | 1–5 DET  | 6–19 DET  | 20+ DET |
|--------------------|----------|-----------|---------|
| **0–1 FTR**        | Baja     | Baja      | Media   |
| **2–3 FTR**        | Baja     | Media     | Alta    |
| **4+ FTR**         | Media    | Alta      | Alta    |

### 4.2 Clasificación de Complejidad por Función

#### Archivos Lógicos Internos (ILF)

| ID    | ILF          | DET | RET | Complejidad | Peso |
|-------|--------------|-----|-----|-------------|------|
| ILF-1 | Usuarios     | 5   | 1   | **Baja**    | 7    |
| ILF-2 | Eventos      | 9   | 1   | **Baja**    | 7    |
| ILF-3 | API Stats    | 6   | 1   | **Baja**    | 7    |

| Complejidad | Cantidad | Peso unitario | Subtotal |
|-------------|----------|---------------|----------|
| Baja        | 3        | 7             | **21**   |
| Media       | 0        | 10            | 0        |
| Alta        | 0        | 15            | 0        |
| **Total ILF** | **3**  |               | **21**   |

#### Archivos de Interfaz Externa (EIF)

| ID    | EIF               | DET | RET | Complejidad | Peso |
|-------|-------------------|-----|-----|-------------|------|
| EIF-1 | Imágenes Externas | 1   | 1   | **Baja**    | 5    |

| Complejidad | Cantidad | Peso unitario | Subtotal |
|-------------|----------|---------------|----------|
| Baja        | 1        | 5             | **5**    |
| Media       | 0        | 7             | 0        |
| Alta        | 0        | 10            | 0        |
| **Total EIF** | **1**  |               | **5**    |

#### Entradas Externas (EI)

| ID   | EI                | DET | FTR | Complejidad | Peso |
|------|-------------------|-----|-----|-------------|------|
| EI-1 | Login             | 3   | 1   | **Baja**    | 3    |
| EI-2 | Registro          | 3   | 1   | **Baja**    | 3    |
| EI-3 | Crear Evento      | 9   | 1   | **Baja**    | 3    |
| EI-4 | Editar Evento     | 9   | 1   | **Baja**    | 3    |
| EI-5 | Eliminar Evento   | 2   | 1   | **Baja**    | 3    |
| EI-6 | Logout            | 1   | 1   | **Baja**    | 3    |

| Complejidad | Cantidad | Peso unitario | Subtotal |
|-------------|----------|---------------|----------|
| Baja        | 6        | 3             | **18**   |
| Media       | 0        | 4             | 0        |
| Alta        | 0        | 6             | 0        |
| **Total EI** | **6**   |               | **18**   |

#### Salidas Externas (EO)

| ID   | EO                   | DET | FTR | Complejidad | Peso |
|------|----------------------|-----|-----|-------------|------|
| EO-1 | API Eventos JSON     | 10  | 3   | **Media**   | 5    |
| EO-2 | API Eventos XML      | 10  | 3   | **Media**   | 5    |
| EO-3 | API Eventos TXT      | 10  | 3   | **Media**   | 5    |
| EO-4 | Descargar Eventos    | 11  | 3   | **Media**   | 5    |

| Complejidad | Cantidad | Peso unitario | Subtotal |
|-------------|----------|---------------|----------|
| Baja        | 0        | 4             | 0        |
| Media       | 4        | 5             | **20**   |
| Alta        | 0        | 7             | 0        |
| **Total EO** | **4**   |               | **20**   |

#### Consultas Externas (EQ)

| ID   | EQ                      | DET | FTR | Complejidad | Peso |
|------|-------------------------|-----|-----|-------------|------|
| EQ-1 | Página Login            | 2   | 0   | **Baja**    | 3    |
| EQ-2 | Página Registro         | 2   | 0   | **Baja**    | 3    |
| EQ-3 | Vista Eventos (consumidor)| 11 | 2   | **Media**   | 4    |
| EQ-4 | Dashboard Admin         | 11  | 2   | **Media**   | 4    |
| EQ-5 | API Stats               | 6   | 1   | **Baja**    | 3    |
| EQ-6 | Redirección Home        | 2   | 1   | **Baja**    | 3    |

| Complejidad | Cantidad | Peso unitario | Subtotal |
|-------------|----------|---------------|----------|
| Baja        | 4        | 3             | **12**   |
| Media       | 2        | 4             | **8**    |
| Alta        | 0        | 6             | 0        |
| **Total EQ** | **6**   |               | **20**   |

---

### 4.3 RESUMEN — PUNTOS DE FUNCIÓN SIN AJUSTAR (PFSA)

| Tipo de Función          | Cantidad | Subtotal PF |
|--------------------------|----------|-------------|
| ILF (Archivos Lógicos Internos) | 3 | 21         |
| EIF (Archivos Interfaz Externa) | 1 | 5          |
| EI  (Entradas Externas)         | 6 | 18         |
| EO  (Salidas Externas)          | 4 | 20         |
| EQ  (Consultas Externas)        | 6 | 20         |
| **TOTAL PFSA**                  | **20** | **84** |

> **Puntos de Función Sin Ajustar (PFSA) = 84**

---

## 5. CÁLCULO DE PUNTOS DE FUNCIÓN AJUSTADOS (PFA)

### 5.1 Factores de Ajuste de Valor (VAF)

Se evalúan 14 Características Generales del Sistema (GSC) en una escala de 0 a 5:

| #  | Característica General del Sistema (GSC)          | Valor | Justificación |
|----|---------------------------------------------------|-------|---------------|
| 1  | Comunicación de datos                              | 4     | API REST con múltiples formatos (JSON, XML, TXT), comunicación por HTTP/HTTPS |
| 2  | Procesamiento distribuido                          | 3     | Aplicación en Vercel (serverless) + BD en Aiven (nube separada) |
| 3  | Rendimiento (Performance)                          | 2     | No hay requisitos críticos de rendimiento pero se usa async con FastAPI |
| 4  | Configuración de uso intensivo                     | 2     | Se despliega en Vercel con configuración específica (vercel.json) |
| 5  | Tasa de transacciones                              | 2     | Tráfico moderado esperado, no es un sistema de alta concurrencia |
| 6  | Entrada de datos en línea                          | 4     | Múltiples formularios: login, registro, CRUD de eventos |
| 7  | Eficiencia del usuario final                       | 3     | Interfaz moderna con animaciones, dark mode, diseño responsivo |
| 8  | Actualización en línea                             | 3     | CRUD completo de eventos (crear, editar, eliminar) en tiempo real |
| 9  | Procesamiento complejo                             | 2     | Conversión de formatos (JSON→XML→TXT), generación de API Keys |
| 10 | Reusabilidad                                       | 3     | API REST reutilizable por aplicaciones externas con API Key |
| 11 | Facilidad de instalación                           | 3     | Deploy automático con Vercel + GitHub CI/CD |
| 12 | Facilidad de operación                             | 3     | Panel admin con dashboard de estadísticas y gestión de eventos |
| 13 | Instalación en múltiples sitios                    | 2     | Preparado para nube pero orientado a un solo despliegue |
| 14 | Facilidad de cambio                                | 2     | Código modular (routers, services, templates separados) |
|    | **TOTAL (TDI — Total Degree of Influence)**       | **38** | |

### 5.2 Cálculo del Factor de Ajuste de Valor (VAF)

```
VAF = 0.65 + (0.01 × TDI)
VAF = 0.65 + (0.01 × 38)
VAF = 0.65 + 0.38
VAF = 1.03
```

### 5.3 Cálculo de Puntos de Función Ajustados (PFA)

```
PFA = PFSA × VAF
PFA = 84 × 1.03
PFA = 86.52 ≈ 87
```

> **Puntos de Función Ajustados (PFA) = 86.52 ≈ 87 PF**

---

## 6. ESTIMACIÓN DE ESFUERZO, TIEMPO Y COSTO

### 6.1 Esfuerzo en Horas

Se utiliza el factor estándar de productividad para proyectos web de complejidad media:

- **Factor de productividad:** 8 horas/PF (estándar para proyectos web con Python/FastAPI)

```
Esfuerzo = PFA × Horas por PF
Esfuerzo = 87 × 8
Esfuerzo = 696 horas-persona
```

> **Esfuerzo Total = 696 horas-persona**

### 6.2 Duración del Proyecto

Suponiendo un equipo de desarrollo y jornadas de trabajo:

| Escenario                         | Personas | Horas/día | Días laborales | Meses (~22 días/mes) |
|-----------------------------------|----------|-----------|----------------|----------------------|
| 1 desarrollador, jornada completa | 1        | 8         | 87 días        | ~4 meses             |
| 2 desarrolladores                 | 2        | 8         | 44 días        | ~2 meses             |
| 3 desarrolladores                 | 3        | 8         | 29 días        | ~1.3 meses           |
| 1 desarrollador, medio tiempo     | 1        | 4         | 174 días       | ~8 meses             |

### 6.3 Estimación de Costos

Se consideran tarifas del mercado mexicano para desarrolladores web:

| Concepto                           | Valor                                |
|------------------------------------|--------------------------------------|
| Tarifa por hora (Jr/Mid México)    | **$150 – $250 MXN/hora**            |
| Tarifa por hora (Senior México)    | **$350 – $500 MXN/hora**            |
| Tarifa por hora (Freelance USD)    | **$25 – $50 USD/hora**              |

#### Escenarios de costo:

| Perfil del Desarrollador     | Tarifa/hora | Horas  | **Costo Total**       |
|------------------------------|-------------|--------|-----------------------|
| Junior (MXN)                 | $150 MXN    | 696    | **$104,400 MXN**      |
| Mid-level (MXN)              | $250 MXN    | 696    | **$174,000 MXN**      |
| Senior (MXN)                 | $400 MXN    | 696    | **$278,400 MXN**      |
| Freelance internacional (USD)| $35 USD     | 696    | **$24,360 USD**       |

### 6.4 Costos de Infraestructura (adicionales al desarrollo)

| Servicio                   | Costo Mensual Estimado  | Costo Anual     |
|----------------------------|-------------------------|-----------------|
| Vercel (plan Hobby/Pro)    | $0 – $20 USD            | $0 – $240 USD   |
| Aiven MySQL (plan básico)  | $19 – $49 USD           | $228 – $588 USD |
| Dominio (.com/.mx)         | ~$10 – $15 USD          | ~$10 – $15 USD  |
| **Total infraestructura**  | **$29 – $84 USD/mes**   | **$238 – $843 USD/año** |

---

## 7. RESUMEN EJECUTIVO

```
┌──────────────────────────────────────────────────────┐
│           RESUMEN DE PUNTOS DE FUNCIÓN               │
├──────────────────────────────────────────────────────┤
│  Total funciones identificadas:        20            │
│    ├─ ILF:  3  │  EIF: 1  │  EI: 6                  │
│    ├─ EO:   4  │  EQ:  6                             │
│                                                      │
│  Puntos de Función Sin Ajustar (PFSA):  84           │
│  Factor de Ajuste de Valor (VAF):       1.03         │
│  Puntos de Función Ajustados (PFA):     87           │
│                                                      │
│  Esfuerzo estimado:    696 horas-persona             │
│  Duración (1 dev):     ~4 meses                      │
│  Costo (Mid MXN):      $174,000 MXN                  │
│  Costo (Sr. MXN):      $278,400 MXN                  │
└──────────────────────────────────────────────────────┘
```

---

> **Nota metodológica:** Este análisis sigue el estándar IFPUG (International Function Point Users Group) para el conteo de Puntos de Función versión 4.3. Los factores de ajuste siguen la norma ISO/IEC 20926. Las estimaciones de esfuerzo utilizan factores de productividad estándar de la industria para proyectos de desarrollo web.
