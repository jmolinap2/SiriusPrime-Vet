# Pasos para la instalación del Sistema *Sirius Prime*

**Descarga de Instaladores**: Puedes descargar los instaladores necesarios para Windows desde los siguientes enlaces:
- [Python](https://drive.google.com/file/d/1LkrPbWbDy_slFkV6AhG12cEbTaQ-LjnL/view?usp=drive_link)
- [GTK3 installer](https://drive.google.com/file/d/1jO6cb_OitpMOvvW1R2_0WtwOfl61hckc/view?usp=drive_link)

## Instaladores Recomendados
- **Compilador Python:** [Python3](https://www.python.org/downloads/release/python-396/)
- **IDEs de Programación:** [Visual Studio Code](https://code.visualstudio.com/), [Sublime Text](https://www.sublimetext.com/), [Pycharm](https://www.jetbrains.com/es-es/pycharm/download/#section=windows)
- **Motores de Base de Datos:** [Sqlite Studio](https://github.com/pawelsalawa/sqlitestudio/releases), [PostgreSQL](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads), [MySQL](https://www.apachefriends.org/es/index.html)

## Pasos de Instalación
1. **Descomprimir el proyecto** en una carpeta local.
2. **Crear un entorno virtual:**
   - **Windows:** `python -m venv venv`
   - **Linux:** `virtualenv venv -p python3`
3. **Instalar WeasyPrint:**
   - **Windows:** Descargar e instalar [GTK3](https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases). Asegúrate de agregarlo a las variables de entorno y reiniciar el computador si es necesario.
   - **Linux:** Instalar las [librerías necesarias](https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#linux) para tu distribución.
4. **Activar el entorno virtual:**
   - **Windows:** `cd venv\Scripts\activate.bat`
   - **Linux:** `source venv/bin/activate`
5. **Instalar dependencias del proyecto:** `pip install -r deploy/txt/requirements.txt`
6. **Configurar la base de datos:**
   - `python manage.py makemigrations`
   - `python manage.py migrate`
7. **Inicializar datos del sistema:** `python manage.py start_installation`
8. **Insertar datos de prueba (opcional):** `python manage.py insert_test_data`
9. **Iniciar el servidor:**
   - Local: `python manage.py runserver`
   - Red: `python manage.py runserver 0.0.0.0:8000`

## **Acceso al Sistema**
- **Usuario:** admin
- **Contraseña:** hacker95

**Gracias por adquirir Sirius Prime!** ✅
