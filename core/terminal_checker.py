 # Verifica si la terminal existe en backend
 
from services.api_terminal_service import verificar_terminal_backend
import platform
import uuid

def obtener_hardware_id():
    return str(uuid.getnode())

def terminal_esta_registrada(hardware_id):
    hardware_id = obtener_hardware_id()
    return verificar_terminal_backend(hardware_id)