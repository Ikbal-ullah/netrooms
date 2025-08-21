#  NetRooms — Multi-room TCP Chat 

  

  

A lightweight TCP server + client that supports nicknames, named rooms,

  

thread-safe broadcasting, and simple slash commands (`/list`, `/who`, `/quit`).

  

  

##  Features

  

- Multiple chat rooms with custom names

  

- User nicknames

  

- Thread-safe broadcasting using locks

  

- Slash commands for listing rooms, users, and quitting

  

- Server logging and graceful disconnect handling

  

  

##  Tech

  

- Python

  

- socket

  

- threading + locks

  

- simple text protocol

  

  

##  How to Run

  

1. Start the server:

  

```

python chat_server.py

```

  

2. Start a client

  

In another terminal, you have two options:

  

Option A — Python client (recommended):

  
```

python chat_client.py

  ```

  

Option B — Netcat client (quick test):

```
  
nc 127.0.0.1 5001

  ```


3. Join and chat

  

Enter a nickname when prompted.

  

Use /list to see rooms, /who to see users, /quit to exit.

  

Start chatting in your chosen room!# Netrooms Project
