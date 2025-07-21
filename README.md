# Proyecto de gestión de reserva en restaurante

## Guía de instalación y ejecución (backend)

### 1. Clonar el repositorio

```bash
git clone https://github.com/Bidobelemti/aplicacionesweb-project
cd aplicacionesweb-project
```

### 2. Inicializar el entorno virtual

```bash
python -m venv venv
.\venv\Scripts\activate
```

> [!IMPORTANT]
> Asegúrate de activar el entorno virtual antes de instalar las dependencias para evitar conflictos con otros proyectos.

### 3. Instalar dependencias

```bash
pip install -r .\requirements.txt
```

### 4. Comprobar el estado del servidor

```bash
python .\backend\test_db_connection.py
```

> [!NOTE]
> Se espera obtener la siguiente salida: **"Conexión exitosa con la base de datos de Render!"**

### 5. Iniciar el servidor Backend

```bash
python manage.py runserver
```

> [!TIP]
> El servidor se ejecutará por defecto en `http://127.0.0.1:8000/`. Puedes cambiar el puerto agregando el número al final del comando (ej: `python manage.py runserver 8080`).

## Rutas disponibles para pruebas

> [!NOTE]
> **Rutas principales del API:**
> 
> - **Ruta general:** `http://127.0.0.1:8000/api/`
> 
> **Autenticación:**
> - `POST http://127.0.0.1:8000/api/users/register/`
> - `POST http://127.0.0.1:8000/api/users/login/`
> 
> **Salas:**
> - `GET http://127.0.0.1:8000/api/salas/`
> 
> **Reservas:**
> - `POST http://127.0.0.1:8000/api/reservas/`
> - `GET http://127.0.0.1:8000/api/reservas/mis-reservas/`
> - `DELETE http://127.0.0.1:8000/api/reservas/<id>/`
> 
> **Gestión:**
> - `GET http://127.0.0.1:8000/api/management/menu/`
> - `GET http://127.0.0.1:8000/api/management/waiters/`

> [!WARNING]
> Verifica que la base de datos esté configurada correctamente antes de realizar operaciones de escritura (POST, DELETE).

> [!CAUTION]
> Puede que la base de datos Postgres de Render no funcione bien algunas veces debido a las migraciones.
## Configuración de conexión a la base de datos (pgAdmin)
> [!TIP]
> Para conectarte a la base de datos desde pgAdmin, usa los siguientes parámetros:
> 
> **General tab:**
> - **Name:** Render DB
> 
> **Connection tab:**
> - **Host name/address:** `(Extraer del External Database URL de Render - es la parte que va después del @ en la URL)`
> - **Port:** `5432`
> - **Maintenance DB:** `reservas_salas_db`
> - **Username:** `root`
> - **Password:** `(Obtener desde Render)`
> 
> ### Nota sobre la URL de Conexión
> - La URL de Render tiene la estructura: `postgresql://<usuario>:<contraseña>@<host>/<nombre_db>`
