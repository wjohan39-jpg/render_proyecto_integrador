"""Cifrado de contrasenas (PBKDF2-SHA256) y generacion de tokens de sesion."""
import hashlib
import hmac
import secrets

ITERACIONES = 200_000


def cifrar_contrasena(contrasena: str) -> str:
    sal = secrets.token_hex(16)
    huella = hashlib.pbkdf2_hmac("sha256", contrasena.encode(), bytes.fromhex(sal), ITERACIONES).hex()
    return f"pbkdf2_sha256${ITERACIONES}${sal}${huella}"


def verificar_contrasena(contrasena: str, guardada: str) -> bool:
    try:
        _, iteraciones, sal, huella = guardada.split("$")
        calculada = hashlib.pbkdf2_hmac(
            "sha256", contrasena.encode(), bytes.fromhex(sal), int(iteraciones)
        ).hex()
    except (ValueError, TypeError):
        return False
    return hmac.compare_digest(calculada, huella)


def nuevo_token() -> str:
    return secrets.token_urlsafe(32)
