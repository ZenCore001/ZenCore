# utils/verificacion.py
import requests
import uuid
from config import API_URL

def verificar_conexion_internet():
    try:
        requests.get("https://www.google.com", timeout=5)
        return True
    except:
        return False

def verificar_conexion_backend():
    try:
        r = requests.get(f"{API_URL}/cuenta/ping", timeout=5)
        return r.status_code == 200
    except:
        return False

def obtener_hardware_id():
    return str(uuid.getnode())  # ID único del equipo

def esta_registrado_en_backend(hardware_id):
    try:
        r = requests.get(f"{API_URL}/terminal/verificar?hardware_id={hardware_id}")
        if r.status_code == 200:
            return r.json().get("registrado", False)
        return False
    except:
        return False

def verificar_entorno():
    hardware_id = obtener_hardware_id()
    try:
        response = requests.get(f"http://localhost:8000/api/terminal/verificar?id={hardware_id}", timeout=3)
        data = response.json()

        if response.status_code == 200 and data.get("existe"):
            return {"ruta": "login", "mensaje": "Terminal verificada. Mostrando login..."}
        else:
            return {"ruta": "bienvenida", "mensaje": "Terminal nueva. Mostrando bienvenida..."}
    except requests.exceptions.RequestException:
        return {"ruta": "bienvenida", "mensaje": "No hay conexión. Trabajando en modo local."}