# Proyecto integrador: registros

Proyecto en Python para simular, exportar, limpiar, consultar y graficar registros de inscripcion.

## Estructura

```text
data/
  crudo/       CSV, XLSX y JSON generados
  limpio/      CSV limpio, cinco consultas y CSV adjunto de referencia
reportes/      tres graficas PNG
src/notebook/  modulos por etapa del procesamiento
```

## Requisitos y ejecucion

Se recomienda Python 3.12 o posterior. Crea y activa un entorno virtual, instala las dependencias y ejecuta el flujo completo:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python main.py
```

El proceso es reproducible en su logica de generacion y crea las carpetas de salida automaticamente. Para ejecutar una etapa por separado:

```bash
python main.py --etapa exportacion
python main.py --etapa limpieza
python main.py --etapa consultas
python main.py --etapa graficacion
```

## Visor React

La interfaz React muestra las tres imagenes generadas en `reportes/` sin duplicarlas. Ejecuta el backend primero y luego inicia el frontend:

```bash
python main.py
cd frontend
npm install
npm run dev
```

Vite muestra la URL local del visor en la terminal.

Tambien puedes ejecutar directamente cada script:

```bash
python src/notebook/simulacion/simular_registros.py
python src/notebook/exportacion/exportar_registros.py
python src/notebook/limpieza/limpiar_registros.py
python src/notebook/consultas/consultas_registros.py
python src/notebook/graficacion/reporte_registros.py
```

## Datos adjuntos

El archivo recibido se conserva sin cambios en `data/limpio/registros_limpio_adjunto.csv`. Sus nombres de columnas y sus 46 filas no corresponden al esquema de las HU de simulacion y limpieza. El flujo principal genera los datos del esquema requerido (`id`, `fecha_registro`, `observacion`, `estado`, `id_usuario`, `id_reto`) y no reemplaza el archivo de referencia.
