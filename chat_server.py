#!/usr/bin/env python3
import socket, threading, sys, time

HOST = '0.0.0.0'
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 5000

rooms = {}
lock = threading.Lock()

def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}")

def send(conn, text):
    try:
        conn.sendall((text + '\n').encode())
    except Exception:
        pass

def broadcast(room, sender_conn, text):
    with lock:
        for conn, nick in list(rooms.get(room, set())):
            if conn is not sender_conn:
                send(conn, f"{text}")

def handle_client(conn, addr):
    try:
        send(conn, "Welcome! Enter your nickname:")
        nick = conn.recv(1024).decode().strip() or f"user{addr[1]}"
        send(conn, "Enter room name to join:")
        room = conn.recv(1024).decode().strip() or "main"

        with lock:
            rooms.setdefault(room, set()).add((conn, nick))
        log(f"{nick}@{addr} joined room '{room}'")
        broadcast(room, conn, f"[{nick}] has joined the room.")

        send(conn, "Commands: /list /who /quit. Start chatting!")

        while True:
            data = conn.recv(4096)
            if not data:
                break
            msg = data.decode().rstrip()
            if msg.startswith('/'):
                if msg == '/list':
                    with lock:
                        rlist = ', '.join(rooms.keys())
                    send(conn, f"Rooms: {rlist}")
                elif msg == '/who':
                    with lock:
                        users = ', '.join(n for (_, n) in rooms.get(room, []))
                    send(conn, f"Users in {room}: {users}")
                elif msg == '/quit':
                    send(conn, "Bye!")
                    break
                else:
                    send(conn, "Unknown command.")
            else:
                broadcast(room, conn, f"[{nick}] {msg}")
    except Exception as e:
        log(f"Error handling client {addr}: {e}")
    finally:
        with lock:
            if room in rooms:
                rooms[room] = {(c,n) for (c,n) in rooms[room] if c is not conn}
                if not rooms[room]:
                    del rooms[room]
        broadcast(room, conn, f"[{nick}] has left.")
        try:
            conn.close()
        except:
            pass
        log(f"{nick}@{addr} disconnected")

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(5)
    log(f"Server listening on {HOST}:{PORT}")
    try:
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
    except KeyboardInterrupt:
        log("Shutting down.")
    finally:
        s.close()

if __name__ == '__main__':
    main()
