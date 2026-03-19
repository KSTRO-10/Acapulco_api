# EXPLICACIÓN DEL ANÁLISIS DE PUNTOS DE FUNCIÓN
## Proyecto "Acapulco API" — Catálogo Emprendedor Digital

**Fecha:** 12 de Marzo de 2026

---

## ¿QUÉ ES EL ANÁLISIS DE PUNTOS DE FUNCIÓN?

El Análisis de Puntos de Función (APF) es una **técnica de medición de software** reconocida internacionalmente bajo el estándar IFPUG (International Function Point Users Group). Su propósito es **medir el tamaño funcional** de un sistema de software desde la perspectiva del usuario, independientemente de la tecnología utilizada.

En palabras simples: así como medimos un terreno en metros cuadrados o el peso de un objeto en kilogramos, los **Puntos de Función (PF)** son la "unidad de medida" del software. Con esta medida podemos estimar cuánto **tiempo**, **esfuerzo** y **dinero** costará desarrollar un proyecto.

---

## PASO 1: IDENTIFICAR LAS FUNCIONES DEL SISTEMA

Lo primero que hicimos fue analizar todo el código del proyecto Acapulco API y clasificar cada funcionalidad en **5 categorías** definidas por el estándar:

### Funciones de Datos (lo que el sistema ALMACENA)

| Tipo | Significado | Ejemplo en nuestro proyecto |
|------|------------|----------------------------|
| **ILF** (Internal Logical File) | Archivos/tablas que **nuestra aplicación mantiene** (crea, lee, actualiza, elimina) | La tabla `usuarios`, la tabla `eventos`, la tabla `api_stats` |
| **EIF** (External Interface File) | Datos que **otro sistema mantiene** pero que nosotros solo leemos/referenciamos | Las imágenes externas (URLs de placehold.co u otros servidores de imágenes) |

**¿Cómo lo identificamos?** Revisamos el archivo `acapulco_database.sql` y encontramos 3 tablas que nuestra aplicación crea y mantiene (ILF), y 1 fuente de datos externa que solo referenciamos (EIF).

### Funciones Transaccionales (lo que el sistema HACE)

| Tipo | Significado | Ejemplo en nuestro proyecto |
|------|------------|----------------------------|
| **EI** (External Input) | Procesos donde el usuario **ingresa o modifica datos** en el sistema | Login, Registro, Crear evento, Editar evento, Eliminar evento, Logout |
| **EO** (External Output) | Procesos que **generan datos procesados** hacia afuera (incluyen cálculos o transformaciones) | La API REST que convierte eventos a JSON, XML o TXT y además registra estadísticas de uso |
| **EQ** (External Query) | Procesos que **consultan y muestran datos** sin modificarlos ni procesarlos | Ver la página de login, ver el catálogo de eventos, ver el dashboard admin |

**¿Cómo lo identificamos?** Revisamos cada ruta (`@app.get`, `@app.post`, `@router.get`, `@router.post`) en los archivos `main.py`, `admin_routes.py` y `api_routes.py`, y clasificamos cada una.

> **Resultado:** Identificamos **20 funciones** en total: 3 ILF + 1 EIF + 6 EI + 4 EO + 6 EQ.

---

## PASO 2: CONTAR LOS DET (Campos Visibles para el Usuario)

**DET** significa "Data Element Type" o **Tipo de Elemento de Dato**. Es cada campo individual que el usuario puede ver, ingresar o que viaja en una transacción.

### Ejemplo práctico — Formulario "Crear Evento":

Cuando el admin crea un evento, el formulario tiene estos campos visibles:

```
1. nombre          →  "Concierto en la Playa"
2. descripcion     →  "Evento musical con artistas locales"
3. lugar           →  "Playa Condesa"
4. hora            →  "20:00"
5. fecha           →  "2026-04-15"
6. imagen_url      →  "https://ejemplo.com/foto.jpg"
7. categoria       →  "Música"
8. precio          →  "150.00"
9. mensaje_éxito   →  "¡Evento creado con éxito!"
```

**Total DET = 9 campos.** Contamos cada campo del formulario que el usuario ve y con el que interactúa.

### Ejemplo práctico — Tabla `usuarios` (ILF):

```
1. id        →  campo clave primaria (auto-generado)
2. username  →  "adminapiaca"
3. password  →  "654321"
4. rol       →  "admin" / "consumidor"
5. api_key   →  "admin_secret_key_123"
```

**Total DET = 5 campos** almacenados en esa tabla.

---

## PASO 3: CONTAR FTR y RET

### RET (Record Element Types) — Para ILF y EIF

El **RET** es un "subgrupo lógico" dentro de un archivo. En nuestro caso, cada tabla tiene **1 solo tipo de registro**, por ejemplo:
- La tabla `usuarios` solo contiene registros de tipo "usuario" → **1 RET**
- La tabla `eventos` solo contiene registros de tipo "evento" → **1 RET**

Si la tabla `eventos` tuviera subcategorías almacenadas como registros separados (ej. "evento_detalle", "evento_participante"), tendría más RETs.

### FTR (File Types Referenced) — Para EI, EO, EQ

El **FTR** indica **cuántas tablas/archivos lógicos toca** cada transacción.

**Ejemplo — Login (EI-1):**
- Solo consulta la tabla `usuarios` para validar credenciales → **1 FTR**

**Ejemplo — API Eventos JSON (EO-1):**
- Lee la tabla `eventos` (datos a devolver) → FTR 1
- Lee la tabla `usuarios` (para validar la API Key) → FTR 2  
- Escribe en la tabla `api_stats` (registra el consumo) → FTR 3
- **Total = 3 FTRs**

---

## PASO 4: CALCULAR COMPLEJIDAD Y PUNTOS DE FUNCIÓN

### ¿Cómo se determina la complejidad?

Se cruzan los valores DET y FTR/RET en una **matriz de complejidad** definida por IFPUG. Dependiendo de la combinación, cada función se clasifica como **Baja**, **Media** o **Alta**.

### Ejemplo — Crear Evento (EI-3):

```
DET = 9 campos  →  está en el rango 5-15
FTR = 1 tabla   →  está en el rango 0-1

Según la matriz de EI:
┌──────────┬──────────┬──────────┬──────────┐
│ FTR\DET  │  1-4     │  5-15    │  16+     │
├──────────┼──────────┼──────────┼──────────┤
│ 0-1 FTR  │  Baja    │ ►BAJA◄  │  Media   │  ← Nuestro caso
│ 2 FTR    │  Baja    │  Media   │  Alta    │
│ 3+ FTR   │  Media   │  Alta    │  Alta    │
└──────────┴──────────┴──────────┴──────────┘

Resultado: Complejidad BAJA → Peso = 3 PF
```

### Ejemplo — API Eventos JSON (EO-1):

```
DET = 10 campos  →  está en el rango 6-19
FTR = 3 tablas   →  está en el rango 2-3

Según la matriz de EO:
┌──────────┬──────────┬──────────┬──────────┐
│ FTR\DET  │  1-5     │  6-19    │  20+     │
├──────────┼──────────┼──────────┼──────────┤
│ 0-1 FTR  │  Baja    │  Baja    │  Media   │
│ 2-3 FTR  │  Baja    │ ►MEDIA◄ │  Alta    │  ← Nuestro caso
│ 4+ FTR   │  Media   │  Alta    │  Alta    │
└──────────┴──────────┴──────────┴──────────┘

Resultado: Complejidad MEDIA → Peso = 5 PF
```

### Pesos por complejidad según el estándar:

| Tipo | Baja | Media | Alta |
|------|------|-------|------|
| ILF  | 7    | 10    | 15   |
| EIF  | 5    | 7     | 10   |
| EI   | 3    | 4     | 6    |
| EO   | 4    | 5     | 7    |
| EQ   | 3    | 4     | 6    |

### Resultado — Puntos de Función Sin Ajustar (PFSA):

Sumamos todos los pesos:

```
ILF:  3 funciones × 7 (Baja)  = 21
EIF:  1 función   × 5 (Baja)  =  5
EI:   6 funciones × 3 (Baja)  = 18
EO:   4 funciones × 5 (Media) = 20
EQ:   4 Baja×3 + 2 Media×4    = 20
────────────────────────────────────
TOTAL PFSA                     = 84 puntos
```

---

## PASO 5: AJUSTAR LOS PUNTOS DE FUNCIÓN

### ¿Por qué se ajustan?

Los PFSA solo miden la funcionalidad "cruda". Pero el esfuerzo real de un proyecto depende de factores técnicos como: ¿el sistema se comunica por red?, ¿tiene múltiples servidores?, ¿el diseño es complejo?, etc.

### Los 14 Factores de Ajuste

El estándar define 14 características que se evalúan de **0 (sin influencia)** a **5 (influencia fuerte)**:

| Factor | Qué evalúa | Nuestro valor | ¿Por qué? |
|--------|------------|---------------|------------|
| 1. Comunicación de datos | ¿Hay APIs, protocolos de red? | 4 | Tenemos API REST multi-formato |
| 2. Procesamiento distribuido | ¿Hay varios servidores? | 3 | App en Vercel + BD en Aiven |
| 3. Rendimiento | ¿Hay requisitos de velocidad? | 2 | No es crítico pero usamos FastAPI |
| 4. Configuración intensiva | ¿Se configura para distintos entornos? | 2 | Config de Vercel + variables de entorno |
| 5. Tasa de transacciones | ¿Alto volumen de operaciones? | 2 | Tráfico moderado |
| 6. Entrada de datos en línea | ¿Hay formularios web? | 4 | Login + Registro + CRUD eventos |
| 7. Eficiencia del usuario | ¿La interfaz es amigable? | 3 | UI moderna con animaciones y dark mode |
| 8. Actualización en línea | ¿Se modifican datos en tiempo real? | 3 | CRUD completo de eventos |
| 9. Procesamiento complejo | ¿Hay lógica de negocio compleja? | 2 | Conversión formatos + API Keys |
| 10. Reusabilidad | ¿Otros sistemas pueden usar el código? | 3 | La API REST es reutilizable |
| 11. Facilidad de instalación | ¿Es fácil de desplegar? | 3 | Deploy automático GitHub→Vercel |
| 12. Facilidad de operación | ¿Es fácil de administrar? | 3 | Dashboard admin con estadísticas |
| 13. Múltiples sitios | ¿Se instala en varios lugares? | 2 | Un solo despliegue en Vercel |
| 14. Facilidad de cambio | ¿Es fácil de modificar? | 2 | Código modular con routers y servicios |

**Suma total (TDI) = 38**

### Fórmula del Factor de Ajuste:

```
VAF = 0.65 + (0.01 × 38) = 1.03
```

Esto significa que el proyecto es un **3% más complejo** que un sistema promedio base.

### Puntos de Función Ajustados:

```
PFA = 84 × 1.03 = 86.52 ≈ 87 Puntos de Función
```

---

## PASO 6: CALCULAR TIEMPO Y COSTO

### ¿Cómo se pasa de Puntos de Función a horas?

Se usa un **factor de productividad** que indica cuántas horas se tardan en implementar 1 PF. Para proyectos web con Python/FastAPI, el estándar de la industria es **8 horas por PF**.

```
Esfuerzo = 87 PF × 8 horas/PF = 696 horas
```

### ¿Cuánto tiempo toma?

Si un desarrollador trabaja 8 horas al día, 22 días al mes:

```
696 horas ÷ 8 horas/día = 87 días laborales
87 días ÷ 22 días/mes ≈ 4 meses
```

Con 2 desarrolladores se reduce a ~2 meses. Con 3, a poco más de 1 mes.

### ¿Cuánto cuesta?

Multiplicamos las 696 horas por la tarifa del desarrollador:

```
Junior:  696 hrs × $150 MXN = $104,400 MXN
Mid:     696 hrs × $250 MXN = $174,000 MXN
Senior:  696 hrs × $400 MXN = $278,400 MXN
```

A esto se suman costos mensuales de infraestructura (Vercel + Aiven) de aproximadamente **$29–$84 USD al mes**.

---

## CONCLUSIÓN

El proyecto Acapulco API, con sus 20 funciones identificadas y 87 Puntos de Función Ajustados, es un sistema de **tamaño pequeño-mediano** según los estándares de la industria. El análisis nos permitió determinar de manera objetiva y cuantificable que:

1. **El proyecto requiere ~696 horas** de esfuerzo de desarrollo
2. **Un solo desarrollador lo completaría en ~4 meses**
3. **El costo estimado oscila entre $104,400 y $278,400 MXN**, dependiendo del nivel del desarrollador

Esta métrica es valiosa porque es **independiente de la tecnología** — si se hubiera construido con Node.js, Java o PHP, los Puntos de Función serían los mismos, ya que miden lo que hace el software, no cómo lo hace.
