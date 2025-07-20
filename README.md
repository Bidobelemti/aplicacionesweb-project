# Proyecto de gestión de reserva en restaurante

# Guía de instalación y ejecución (backend)

## 1.  Clonar el repositorio

```bash
git clone https://github.com/Bidobelemti/aplicacionesweb-project
cd aplicacionesweb-project

```
## 2. Inicializar el entorno virtual

```bash
python -m venv venv
.\venv\Scripts\activate

```

## 3. Instalar dependencias 

```bash
pip install -r .\requirements.txt

```

## 4. Comprobar el estado del servidor

```bash
python .\backend\test_db_connection.py

```

Se espera que lleguemos a obtener la siguiente salida
Conexión exitosa con la base de datos de Render!
