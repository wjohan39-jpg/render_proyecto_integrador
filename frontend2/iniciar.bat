@echo off
setlocal
cd /d "%~dp0"

where node >nul 2>nul
if errorlevel 1 (
  echo.
  echo [ERROR] Node.js no esta instalado o no esta en el PATH.
  echo Descargalo desde https://nodejs.org y vuelve a intentar.
  echo.
  pause
  exit /b 1
)

where npm >nul 2>nul
if errorlevel 1 (
  echo.
  echo [ERROR] npm no esta disponible.
  echo Reinstala Node.js desde https://nodejs.org
  echo.
  pause
  exit /b 1
)

if not exist "node_modules\vite\package.json" (
  echo.
  echo Instalando dependencias por primera vez...
  echo.
  call npm install
  if errorlevel 1 (
    echo.
    echo [ERROR] No se pudieron instalar las dependencias.
    echo Revisa tu conexion a internet e intenta de nuevo.
    echo.
    pause
    exit /b 1
  )
)

echo.
echo Iniciando Proyecto Integrador Cesde en el navegador...
echo Para detener el servidor presiona Ctrl+C.
echo.
call npm start
