import os
import django
from django.db import connections
from django.db.utils import OperationalError

# 🔧 Esto le dice a Django dónde está tu archivo de configuración
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "model.settings")
django.setup()

# 🧪 Probar conexión
db_conn = connections['default']
try:
    db_conn.cursor()
    print("Conexión exitosa con la base de datos de Render!")
except OperationalError as e:
    print("Error de conexión:", e)
