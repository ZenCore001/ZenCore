# core/splash/verificar_terminal.py

import requests
import uuid
from config import BACKEND_URL

def obtener_hardware_id():
    # Simulación para pruebas
    return str(uuid.getnode())

def registrar_terminal(correo_contacto: str, nombre_terminal: str = None):
    url = f"{BACKEND_URL}/api/terminal/registrar-terminal"
    hardware_id = obtener_hardware_id()
    
    payload = {
        "hardware_id": hardware_id,
        "correo_contacto": correo_contacto,
        "nombre": nombre_terminal or f"ZEN-TEMP-{hardware_id[-4:]}"
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        return {
            "success": True,
            "cuenta_id": data["cuenta_id"],
            "nombre_terminal": data["nombre"],
            "hardware_id": hardware_id
        }
    except requests.HTTPError as err:
        return {
            "success": False,
            "error": str(err),
            "status_code": response.status_code,
            "detail": response.json().get("detail")
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }