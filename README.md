# Proyecto integrador

Proyecto unificado de cuatro desarrolladores. Cada uno trabajó una tabla con el mismo flujo: **simular → exportar → limpiar → consultar → graficar**.

| Sección | Desarrollador | Archivos |
|---|---|---|
| Prioridades | Dave | `*_prioridades.py`, `limpiar_prioridad.py`, `prioridades_*` |
| Registros | Jeferson | `*_registros.py`, `registros_*` |
| Empresas | Wesly | `*_empresas.py`, `empresas_*` |
| Retos | Diego | `*_reto.py`, `retos_*` |

El proyecto tiene tres partes:

1. **Backend de datos** (`main.py` + `src/notebook/`): genera los CSV y las gráficas.
2. **API REST** (`api/`, FastAPI): sirve esos resultados como JSON e imágenes, y ofrece inicio de sesión y un CRUD sobre una base de datos (MySQL, Postgres o SQLite).
3. **Aplicación web** (`frontend/`, React + Vite, JavaScript): inicio de sesión, panel (dashboard) y pantallas de empresas, prioridades, retos, registros y usuarios, que consumen la API.

## En línea (Render)

| Servicio | URL |
|---|---|
| Aplicación web | https://proyecto-integrador-0i4w.onrender.com |
| API | https://proyecto-integrador-api-n977.onrender.com |
| Documentación de la API | https://proyecto-integrador-api-n977.onrender.com/docs |

La API usa el plan gratuito: si pasa ~15 minutos sin recibir visitas se apaga, y la primera petición siguiente puede tardar hasta un minuto.

Cada `git push` a `main` vuelve a desplegar ambos servicios automáticamente (la app de Render está instalada en el repositorio de GitHub).

### Base de datos

En Render, la API guarda el CRUD (usuarios, empresas, prioridades, retos y registros) en la base **Render Postgres** `proyecto-integrador-db`. El servicio de la API la recibe en la variable de entorno `DATABASE_URL` (la *Internal Database URL* de la base). La primera vez que la API arranca con una base vacía crea las tablas y carga los CSV de `data/limpio/`; después los cambios se conservan entre despliegues.

En local la API usa el **MySQL de XAMPP** (ver [API](#2-api)). SQLite (`data/integrador.db`) solo se usa como último recurso en Render cuando no hay `DATABASE_URL`. Para ver la base de Render desde DBeaver o pgAdmin usa la *External Database URL* (Render → base de datos → **Connect** → **External**).

La base gratuita de Render vence a los 30 días de creada.

## Estructura

```text
main.py                 ejecuta las 5 etapas para las 4 secciones
requirements.txt        dependencias de Python (backend y API)
.python-version         versión de Python que usa Render
data/
  crudo/                CSV, XLSX y JSON simulados (<tabla>_sucio.*)
  limpio/               CSV limpio y cinco consultas por tabla
reportes/               tres gráficas PNG por tabla
docs/
  diagrama_relacional.html   diagrama relacional de las tablas
iniciar_api_mysql.bat   enciende la API con el MySQL de XAMPP (Windows)
src/notebook/
  simulacion/           generan los datos sucios
  exportacion/          guardan CSV, XLSX y JSON en data/crudo
  limpieza/             producen <tabla>_limpio.csv
  consultas/            producen <tabla>_consulta_1..5.csv
  graficacion/          producen reportes/<tabla>_grafica_1..3.png
api/
  app.py                aplicación FastAPI y endpoints de solo lectura
  auth.py               login, registro, sesión actual y logout
  crud.py               CRUD de empresas, prioridades, retos, registros y usuarios
  db.py                 conexión (MySQL / Postgres / SQLite), esquema y carga de los CSV
  esquemas.py           validación de datos (Pydantic)
  seguridad.py          cifrado de contraseñas y tokens
  catalogo.py           textos, gráficas y consultas de cada sección
frontend/src/
  App.jsx, main.jsx     arranque y rutas de la aplicación
  assets/               estilos globales
  modules/
    core/               componentes, design-system, hooks, lib, rutas y utils compartidos
    auth/               inicio de sesión y registro
    dashboard/          panel principal
    empresa/            pages · components · hooks · services (llamadas a la API)
    prioridad/          ...
    registro/           ...
    reto/               ...
    usuario/            ...
```

## Requisitos

- Python 3.12 o posterior
- Node.js 20.19 o posterior (para la aplicación web)
- XAMPP con MySQL encendido (para la API en local)

## Ejecución en local

### 1. Backend de datos

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows (en Linux/macOS: source .venv/bin/activate)
pip install -r requirements.txt
python main.py
```

Para ejecutar una sola etapa:

```bash
python main.py --etapa simulacion
python main.py --etapa exportacion
python main.py --etapa limpieza
python main.py --etapa consultas
python main.py --etapa graficacion
```

`main.py` sobrescribe `data/` y `reportes/` con datos simulados nuevos cada vez que se ejecuta.

### 2. API

Desde la raíz, con el entorno activado:

```bash
uvicorn api.app:app --reload
```

- API: http://127.0.0.1:8000
- Documentación interactiva: http://127.0.0.1:8000/docs

En local la API guarda siempre en el MySQL de XAMPP (base `integrador_relacional`, visible en
phpMyAdmin): enciende MySQL en XAMPP antes de arrancarla. Si la base no existe, la API la crea
y la llena con los CSV limpios. Otra base se indica con `MYSQL_URL`. En Render se usa
`DATABASE_URL` (Postgres). `frontend\iniciar.bat` abre también la API si no está encendida.

En Windows, `iniciar_api_mysql.bat` hace lo mismo con la `MYSQL_URL` ya definida.

La primera vez se crea el usuario administrador `admin@cesde.edu.co` con la contraseña `Admin123*`. Se pueden cambiar con las variables `ADMIN_EMAIL` y `ADMIN_PASSWORD`; conviene hacerlo en Render.

### 3. Aplicación web

En otra terminal:

```bash
cd frontend
npm install
npm run dev
```

En Windows también puedes ejecutar `frontend\iniciar.bat`, que instala las dependencias, enciende la API si hace falta y abre el navegador.

Por defecto la aplicación consume la API local (`http://127.0.0.1:8000`). Para usar otra, crea `frontend/.env` a partir de `frontend/.env.example` y cambia `VITE_API_URL`.

## API

Hay dos grupos de endpoints. La documentación interactiva completa está en `/docs`.

### Resultados del análisis (públicos, solo lectura)

Todos son `GET` y no piden sesión. `{modulo}` puede ser `prioridades`, `registros`, `empresas` o `retos`.

| Endpoint | Respuesta |
|---|---|
| `/api/salud` | `{"estado": "ok"}` |
| `/api/modulos` | Lista de secciones (`id`, `nombre`, `autor`) |
| `/api/modulos/{modulo}` | Textos, total de registros, gráficas y consultas de la sección |
| `/api/modulos/{modulo}/consultas/{1-5}` | `titulo`, `columnas`, `total` y `filas` de la consulta |
| `/api/modulos/{modulo}/datos?pagina=1&tamano=20` | Datos limpios paginados (`tamano` máximo 200) |
| `/api/modulos/{modulo}/graficas/{1-3}` | Imagen PNG |

Si la sección o el número no existen, responde `404` con el motivo en `detail`.

Ejemplo:

```js
const res = await fetch("https://proyecto-integrador-api-n977.onrender.com/api/modulos/retos/consultas/1");
const { titulo, columnas, filas, total } = await res.json();
```

### Sesión y CRUD (piden sesión iniciada)

| Endpoint | Descripción |
|---|---|
| `POST /api/auth/login`, `POST /api/auth/register` | Iniciar sesión (devuelve un token) y registrarse |
| `GET /api/auth/me`, `POST /api/auth/logout` | Usuario de la sesión y cierre de sesión |
| `/api/{empresas,prioridades,retos,registros}` | `GET` lista, `GET /{id}`, `POST`, `PUT /{id}`, `DELETE /{id}` |
| `/api/usuarios` | Igual que los anteriores, solo para el rol administrador |

El token se envía en la cabecera `Authorization: Bearer <token>` y vence a las 8 horas. Con MySQL, las claves foráneas rechazan (422) los ids que no existen en su tabla.

La variable de entorno `CORS_ORIGINS` (orígenes separados por comas) limita qué páginas pueden llamar a la API; por defecto se permiten todas.

## Publicar cambios

1. Si cambian los datos, ejecuta `python main.py`.
2. Sube los cambios:

   ```bash
   git add -A
   git commit -m "Describe el cambio"
   git push
   ```

Render despliega la API y el visor en uno o dos minutos. Si algún día no lo hace, en el [panel de Render](https://dashboard.render.com) usa **Manual Deploy → Deploy latest commit** en cada servicio.

Render no ejecuta `main.py`: publica los CSV y PNG que estén en el repositorio. Tampoco puede usar el MySQL de XAMPP: allí la API usa Postgres.

## Datos adjuntos

El archivo recibido se conserva sin cambios en `data/limpio/registros_limpio_adjunto.csv`. Sus nombres de columnas y sus 46 filas no corresponden al esquema de las HU de simulación y limpieza. El flujo principal genera los datos del esquema requerido (`id`, `fecha_registro`, `observacion`, `estado`, `id_usuario`, `id_reto`) y no reemplaza el archivo de referencia.
