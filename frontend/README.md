# Frontend 2 · Gestión del Proyecto Integrador Cesde

Interfaz en React 19 + Vite 7 con el diseño del visor (`../frontend`): colores Cesde,
General Sans + DM Mono, fondo animado y paneles con efecto vidrio.
Consume la **API FastAPI** de `../api`.

Permite iniciar sesión, registrarse, salir y, en cada módulo, **consultar (buscar y filtrar),
crear, modificar y eliminar**: empresas, prioridades, retos, registros y usuarios (solo administradores).
Cada módulo tiene además la vista **Reporte** con las gráficas y consultas que genera `main.py`.

## Cómo ejecutarlo

1. **API** (desde la raíz del proyecto):

   ```bash
   pip install -r requirements.txt
   uvicorn api.app:app --reload        # http://127.0.0.1:8000  (docs en /docs)
   ```

   La primera vez crea `data/integrador.db` (SQLite) y la llena con los CSV de `data/limpio/`.
   Para empezar de cero, detén la API y borra ese archivo.

2. **Frontend** (en esta carpeta):

   ```bash
   npm install      # solo la primera vez
   npm run dev      # http://localhost:5173
   ```

   O doble clic en `iniciar.bat`. En desarrollo Vite reenvía `/api` a `http://127.0.0.1:8000`
   (ver `vite.config.js`), así que no hay problemas de CORS.

   Para una compilación que llame a la API directamente: `VITE_API_URL=https://...` (ver `.env.example`).

## Usuario de prueba

| Correo               | Contraseña  | Rol           |
| -------------------- | ----------- | ------------- |
| `admin@cesde.edu.co` | `Admin123*` | Administrador |

Se puede cambiar con las variables `ADMIN_EMAIL` y `ADMIN_PASSWORD` de la API (antes de crear la base).
El registro público solo crea empresarios y profesores; los administradores se crean desde **Usuarios**.

## Páginas

| Ruta           | Página                                   | Acceso        |
| -------------- | ---------------------------------------- | ------------- |
| `/login`       | Iniciar sesión                           | Pública       |
| `/registro`    | Crear cuenta                             | Pública       |
| `/dashboard`   | Panel con el resumen de los módulos      | Con sesión    |
| `/empresas`    | CRUD + reporte (`?vista=reporte`)        | Con sesión    |
| `/prioridades` | CRUD + reporte                           | Con sesión    |
| `/retos`       | CRUD + reporte                           | Con sesión    |
| `/registros`   | CRUD + reporte                           | Con sesión    |
| `/usuarios`    | CRUD de usuarios                         | Administrador |

## Endpoints que usa

| Método | Ruta                                   | Uso                                 |
| ------ | -------------------------------------- | ----------------------------------- |
| POST   | `/api/auth/login` · `/api/auth/register` | Devuelven `{ token, usuario }`    |
| GET    | `/api/auth/me`                         | Restaura la sesión al recargar      |
| POST   | `/api/auth/logout`                     | Cierra la sesión en la API          |
| GET/POST | `/api/{recurso}`                     | Listar / crear                      |
| GET/PUT/DELETE | `/api/{recurso}/{id}`          | Consultar / modificar / eliminar    |
| GET    | `/api/modulos/{id}` y `/consultas/{n}` | Reportes de `main.py`               |

`{recurso}` = `empresas`, `prioridades`, `retos`, `registros`, `usuarios`.
El token se guarda en `localStorage` y viaja en `Authorization: Bearer <token>`; vence a las 8 horas.

## Estructura (screaming architecture)

```
src/
├── App.jsx                  rutas
├── main.jsx
├── assets/styles.css        identidad visual (la misma del visor)
└── modules/
    ├── core/
    │   ├── components/      LayoutPrivado, BarraSuperior, NavegacionModulos, FondoAnimado,
    │   │                    Introduccion, PaginaModulo, GestionCrud, SeccionReporte, PanelConsultas…
    │   ├── design-system/   Boton, Input, Select, Textarea, Casilla, Modal, Confirmacion, Aviso,
    │   │                    EstadoCarga, Etiqueta, TablaCrud, TablaDatos, Paginacion, TarjetaGrafica
    │   ├── hooks/           useCrud, useFormulario, usePeticion, useTablaFiltrada
    │   ├── lib/             apiClient, crudService, reportesApi, menu, storage
    │   ├── routes/          PrivateRoute, PublicRoute, AdminRoute
    │   └── utils/           formato, validaciones, opciones
    ├── auth/                login, registro y sesión
    ├── dashboard/           panel de inicio
    ├── empresa/  prioridad/  reto/  registro/  usuario/
```

Cada módulo de datos tiene la misma forma:

```
empresa/
├── components/   EmpresaForm.jsx, columnasEmpresa.jsx
├── hooks/        useEmpresas.js            (useCrud + servicio)
├── lib/          constantes.js             (sectores, estados…)
├── pages/        EmpresasPage.jsx          (PaginaModulo + GestionCrud)
├── services/     empresaService.js         (crearCrudService('empresas'))
└── utils/        validarEmpresa.js         (validación y limpieza antes de enviar)
```

## Notas

- Las gráficas y consultas del **Reporte** salen de los CSV de `main.py`; no cambian con el CRUD.
- Los datos simulados tienen IDs de relación que no coinciden entre tablas (por ejemplo, un reto
  apunta a una empresa que no existe); en esos casos la tabla muestra el ID corto y el formulario
  lo conserva como "sin coincidencia".
