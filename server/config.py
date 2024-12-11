import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Acceder a la configuración
REDIS_URL = os.getenv("REDIS_URL")

# Verificar que REDIS_URL esté cargado
if not REDIS_URL:
    raise ValueError("REDIS_URL no está configurado en el archivo .env")