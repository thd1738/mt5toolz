import base64
import os
from datetime import datetime, timedelta, timezone

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.padding import PKCS7
from jose import jwt

from app.core.config import settings


class CryptoService:
    def __init__(self, key: str):
        self.key = key.encode("utf-8")

    def encrypt(self, plaintext: str) -> str:
        iv = os.urandom(16)
        padder = PKCS7(128).padder()
        padded = padder.update(plaintext.encode("utf-8")) + padder.finalize()
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(padded) + encryptor.finalize()
        return base64.b64encode(iv + ciphertext).decode("utf-8")

    def decrypt(self, encoded: str) -> str:
        payload = base64.b64decode(encoded)
        iv, ciphertext = payload[:16], payload[16:]
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        padded = decryptor.update(ciphertext) + decryptor.finalize()
        unpadder = PKCS7(128).unpadder()
        plaintext = unpadder.update(padded) + unpadder.finalize()
        return plaintext.decode("utf-8")


crypto_service = CryptoService(settings.aes_key)


def create_access_token(subject: str, expires_minutes: int = 60) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": subject,
        "iat": now,
        "exp": now + timedelta(minutes=expires_minutes),
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)
