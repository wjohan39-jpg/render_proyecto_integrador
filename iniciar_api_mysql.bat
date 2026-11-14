@echo off
REM Inicia la API usando el MySQL de XAMPP (base integrador_relacional).
REM Antes enciende MySQL en el panel de XAMPP.
cd /d "%~dp0"
set MYSQL_URL=mysql://root@127.0.0.1:3306/integrador_relacional
python -m uvicorn api.app:app --reload
