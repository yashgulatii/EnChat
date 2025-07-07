import subprocess
import sys
import os

def start_server():
    server_path = os.path.join("backend", "server.py")
    print("\n[INFO] Starting EnChat server...\n")
    subprocess.run([sys.executable, server_path])

def start_client_gui():
    # gui_path = os.path.join("frontend", "gui.py")
    print("\n[INFO] Starting EnChat client (GUI)...\n")
    subprocess.run([sys.executable, "-m", "frontend.gui"])

def main():
    print("""
===========================
  EnChat - Secure Messenger
===========================

Start as:
1. Server
2. Client
    """)

    choice = input("Enter 1 for Server or 2 for Client: ").strip()

    if choice == '1':
        start_server()
    elif choice == '2':
        start_client_gui()
    else:
        print("❌ Invalid choice. Please enter 1 or 2.\n")
        main()

if __name__ == "__main__":
    main()
