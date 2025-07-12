# api_terminal_service.py
import requests
from config import BACKEND_URL  # ✅ Se importa directamente desde config.py

def verificar_terminal_backend(hardware_id):
    try:
        response = requests.get(f"{BACKEND_URL}/api/terminal/existe/{hardware_id}", timeout=5)
        if response.status_code == 200:
            return response.json().get("existe", False)
    except Exception as e:
        print(f"[ERROR] Verificación de terminal fallida: {e}")
    return False