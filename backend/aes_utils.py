from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
import hashlib

def pad(data):
    return data + (16 - len(data) % 16) * chr(16 - len(data) % 16)

def unpad(data):
    return data[:-ord(data[-1])]

def encrypt_message(key, message):
    key = hashlib.sha256(key.encode()).digest()
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted = cipher.encrypt(pad(message).encode())
    return base64.b64encode(iv + encrypted).decode()

def decrypt_message(key, enc_data):
    key = hashlib.sha256(key.encode()).digest()
    enc_data = base64.b64decode(enc_data.encode())
    iv = enc_data[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = cipher.decrypt(enc_data[16:])
    return unpad(decrypted.decode())
