# utils/servidor_check.py
import requests
from config import BACKEND_URL

def servidor_esta_activo():
    try:
        response = requests.get(f"{BACKEND_URL}/api/cuenta/ping", timeout=3)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False