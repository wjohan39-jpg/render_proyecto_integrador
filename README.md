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
2. **API REST** (`api/`, FastAPI): sirve esos resultados como JSON e imágenes.
3. **Visor web** (`frontend/`, React + Vite + TypeScript): consume la API.

## En línea (Render)

| Servicio | URL |
|---|---|
| Visor web | https://proyecto-integrador-0i4w.onrender.com |
| API | https://proyecto-integrador-api-n977.onrender.com |
| Documentación de la API | https://proyecto-integrador-api-n977.onrender.com/docs |

La API usa el plan gratuito: si pasa ~15 minutos sin recibir visitas se apaga, y la primera petición siguiente puede tardar hasta un minuto.

Cada `git push` a `main` vuelve a desplegar ambos servicios automáticamente.

## Estructura

```text
main.py                 ejecuta las 5 etapas para las 4 secciones
requirements.txt        dependencias de Python (backend y API)
.python-version         versión de Python que usa Render
data/
  crudo/                CSV, XLSX y JSON simulados (<tabla>_sucio.*)
  limpio/               CSV limpio y cinco consultas por tabla
reportes/               tres gráficas PNG por tabla
src/notebook/
  simulacion/           generan los datos sucios
  exportacion/          guardan CSV, XLSX y JSON en data/crudo
  limpieza/             producen <tabla>_limpio.csv
  consultas/            producen <tabla>_consulta_1..5.csv
  graficacion/          producen reportes/<tabla>_grafica_1..3.png
api/
  app.py                endpoints de FastAPI
  catalogo.py           textos, gráficas y consultas de cada sección
frontend/src/
  assets/               estilos globales
  modules/
    core/               componentes, design-system, hooks, lib y utils compartidos
    prioridades/        components · hooks · services (llamadas a la API)
    registros/          ...
    empresas/           ...
    retos/              ...
```

## Requisitos

- Python 3.12 o posterior
- Node.js 20 o posterior (para el visor)

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

### 3. Visor web

En otra terminal:

```bash
cd frontend
npm install
npm run dev
```

Por defecto el visor consume la API local (`http://127.0.0.1:8000`). Para usar otra, crea `frontend/.env` a partir de `frontend/.env.example` y cambia `VITE_API_URL`.

## API

Todos los endpoints son `GET`, públicos y de solo lectura. `{modulo}` puede ser `prioridades`, `registros`, `empresas` o `retos`.

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

La variable de entorno `CORS_ORIGINS` (orígenes separados por comas) limita qué páginas pueden llamar a la API; por defecto se permiten todas.

## Publicar cambios

1. Si cambian los datos, ejecuta `python main.py`.
2. Sube los cambios:

   ```bash
   git add -A
   git commit -m "Describe el cambio"
   git push
   ```

Render no ejecuta `main.py`: publica los CSV y PNG que estén en el repositorio.

## Datos adjuntos

El archivo recibido se conserva sin cambios en `data/limpio/registros_limpio_adjunto.csv`. Sus nombres de columnas y sus 46 filas no corresponden al esquema de las HU de simulación y limpieza. El flujo principal genera los datos del esquema requerido (`id`, `fecha_registro`, `observacion`, `estado`, `id_usuario`, `id_reto`) y no reemplaza el archivo de referencia.
