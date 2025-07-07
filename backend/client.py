import socket
import threading
from backend.aes_utils import encrypt_message, decrypt_message
from backend.rsa_utils import generate_keys

HOST = '127.0.0.1'
PORT = 9999

# Simulate secure key exchange
shared_key = "my_shared_secret"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

def receive():
    while True:
        try:
            message = client.recv(4096).decode()
            print("Encrypted:", message)
            print("Decrypted:", decrypt_message(shared_key, message))
        except:
            print("[ERROR] Disconnected from server.")
            break

def write():
    while True:
        msg = input("")
        encrypted = encrypt_message(shared_key, msg)
        client.send(encrypted.encode())

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
