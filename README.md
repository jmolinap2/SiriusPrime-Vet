# **Instalación del Sistema Sirius Prime**

**Enlaces para la descarga de instaladores** (Windows):
- **Python:** [Descargar Python](https://drive.google.com/file/d/1LkrPbWbDy_slFkV6AhG12cEbTaQ-LjnL/view?usp=drive_link)
- **GTK3 Installer:** [Descargar GTK3](https://drive.google.com/file/d/1jO6cb_OitpMOvvW1R2_0WtwOfl61hckc/view?usp=drive_link)

## **Instaladores Recomendados**
- **Compilador Python:** [Python3.9.6](https://www.python.org/downloads/release/python-396/)
- **IDE de programación:** [Visual Studio Code](https://code.visualstudio.com/), [Sublime Text](https://www.sublimetext.com/), [PyCharm](https://www.jetbrains.com/es-es/pycharm/download/#section=windows)
- **Motores de Base de Datos:** [SQLite Studio](https://github.com/pawelsalawa/sqlitestudio/releases), [PostgreSQL](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads), [MySQL](https://www.apachefriends.org/es/index.html)

## **Pasos de Instalación**
1. **Descomprimir el proyecto** en una carpeta local.
2. **Crear un entorno virtual:**
   - **Windows:**
     ```bash
     python -m venv venv
     ```
   - **Linux:**
     ```bash
     virtualenv venv -p python3
     ```

3. **Instalar WeasyPrint:**
   - **Windows:** Descargar e instalar [GTK3](https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases). Asegurarse de agregarlo a las variables de entorno y reiniciar el computador si es necesario.
   - **Linux:** Instalar las [librerías necesarias](https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#linux) para tu distribución.

4. **Activar el entorno virtual:**
   - **Windows:**
     ```bash
     cd venv\Scripts\activate.bat
     ```
   - **Linux:**
     ```bash
     source venv/bin/activate
     ```

5. **Instalar dependencias del proyecto:**
   ```bash
   pip install -r deploy/txt/requirements.txt


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
