#!/usr/bin/env python3
import socket, threading, sys

if len(sys.argv) < 3:
    print("Usage: python3 chat_client.py HOST PORT")
    sys.exit(1)

HOST = sys.argv[1]
PORT = int(sys.argv[2])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

def listen():
    try:
        while True:
            data = s.recv(4096)
            if not data:
                break
            print(data.decode().rstrip())
    except Exception:
        pass
    finally:
        print("Connection closed.")
        sys.exit(0)

threading.Thread(target=listen, daemon=True).start()

for _ in range(2):
    prompt = s.recv(4096).decode().strip()
    print(prompt)
    ans = input()
    s.sendall((ans + '\n').encode())

print("You can now chat. Use /quit to exit.")
try:
    while True:
        line = input()
        s.sendall((line + '\n').encode())
        if line.strip() == '/quit':
            break
except KeyboardInterrupt:
    pass
finally:
    s.close()
