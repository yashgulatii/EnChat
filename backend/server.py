import socket
import threading

clients = []

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    while True:
        try:
            msg = conn.recv(4096)
            if not msg:
                break
            broadcast(msg, conn)
        except:
            break
    conn.close()
    clients.remove(conn)
    print(f"[DISCONNECTED] {addr} disconnected.")

def broadcast(msg, sender_conn):
    for client in clients:
        if client != sender_conn:
            try:
                client.send(msg)
            except:
                clients.remove(client)

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Doesn't have to be reachable, just used to get interface IP
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

def start_server(host='0.0.0.0', port=9999):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()
    local_ip = get_local_ip()
    print(f"[SERVER STARTED] Listening on {local_ip}:{port} (accessible on LAN)")
    while True:
        conn, addr = server.accept()
        clients.append(conn)
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    start_server()
