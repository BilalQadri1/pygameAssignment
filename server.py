import socket
import threading
import pickle
import struct
import json # <--- ADD THIS HERE
server = "0.0.0.0" # Keeps it open for AWS/Cloud hosting
port = 5555
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((server, port))
s.listen()

lobbies = {}
lobby_id_counter = 0
file_lock = threading.Lock() # <--- ADD THIS

def send_data(conn, data):
    # Safely package and send data with a length header
    try:
        packed_data = pickle.dumps(data)
        header = struct.pack('I', len(packed_data))
        conn.sendall(header + packed_data)
    except Exception as e:
        print(f"Send error: {e}")

def recv_data(conn):
    # Safely read the length header, then the exact data
    try:
        raw_msglen = recvall(conn, 4)
        if not raw_msglen: return None
        msglen = struct.unpack('I', raw_msglen)[0]
        
        raw_data = recvall(conn, msglen)
        if not raw_data: return None
        return pickle.loads(raw_data)
    except Exception as e:
        return None

def recvall(conn, n):
    data = bytearray()
    while len(data) < n:
        packet = conn.recv(n - len(data))
        if not packet: return None
        data.extend(packet)
    return data

def threaded_client(conn):
    global lobby_id_counter
    
    # --- NEW: Track where this specific connection is ---
    current_lobby = None
    current_player = None
    
    # Send welcome handshake
    send_data(conn, "Connected to Server")
    
    while True:
        # Use our new safe receiver
        request = recv_data(conn)
        if not request:
            break # Client disconnected cleanly or crashed
            
        try:
            # ==================================================
            # --- NEW: SERVER DATABASE COMMANDS ---
            if request[0] == "FETCH_DATA":
                file_name = request[1]
                try:
                    with file_lock: # <--- LOCK THE FILE
                        with open(file_name, "r") as f:
                            file_data = json.load(f)
                    send_data(conn, file_data)
                except (FileNotFoundError, json.JSONDecodeError):
                    if file_name == "market_listings.json":
                        send_data(conn, [])
                    else:
                        send_data(conn, {})

            elif request[0] == "SAVE_DATA":
                file_name = request[1]
                file_payload = request[2]
                
                with file_lock: # <--- LOCK THE FILE
                    with open(file_name, "w") as f:
                        json.dump(file_payload, f, indent=4)
                        
                send_data(conn, "SAVED")
            # ==================================================

            # --- CHANGE THIS FROM 'if' TO 'elif' ---
            elif request[0] == "GET":
                summary = {id: len([p for p in info["players"] if p is not None]) for id, info in lobbies.items()}
                send_data(conn, summary)

            elif request[0] == "CREATE":
                lobby_id_counter += 1
                new_id = lobby_id_counter
                lobbies[new_id] = {"players": [None] * 10}
                lobbies[new_id]["players"][0] = request[1] 
                
                # Remember that this connection owns this slot
                current_lobby = new_id
                current_player = 0
                
                send_data(conn, [new_id, 0]) 

            elif request[0] == "JOIN":
                l_id = request[1]
                if l_id in lobbies:
                    p_id = -1
                    for i, p in enumerate(lobbies[l_id]["players"]):
                        if p is None:
                            p_id = i
                            break
                    if p_id != -1:
                        lobbies[l_id]["players"][p_id] = request[2]
                        
                        # Remember that this connection owns this slot
                        current_lobby = l_id
                        current_player = p_id
                        
                        send_data(conn, [l_id, p_id])
                    else:
                        send_data(conn, "FULL")
                else:
                    send_data(conn, "NOT_FOUND")

            elif request[0] == "LEAVE":
                l_id, p_id = request[1], request[2]
                if l_id in lobbies:
                    lobbies[l_id]["players"][p_id] = None
                    
                    # Close lobby ONLY if everyone is gone
                    if all(p is None for p in lobbies[l_id]["players"]):
                        del lobbies[l_id]
                        print(f"Lobby {l_id} closed (Everyone left).")
                        
                current_lobby = None
                current_player = None
                send_data(conn, "OK")

            elif request[0] == "UPDATE":
                l_id, p_id, p_data = request[1], request[2], request[3]
                if l_id in lobbies:
                    lobbies[l_id]["players"][p_id] = p_data
                    send_data(conn, lobbies[l_id]["players"])
                else:
                    send_data(conn, "CLOSED")
                    
        except Exception as e:
            print(f"Command Error: {e}")
            break

    # ==================================================
    # --- CRASH AND CLEANUP LOGIC ---
    # If the loop breaks because of a game crash, remove the player
    if current_lobby is not None and current_lobby in lobbies:
        if current_player is not None:
            lobbies[current_lobby]["players"][current_player] = None
            print(f"Player {current_player} dropped from Lobby {current_lobby}")
        
        # If the lobby is now completely empty, delete it
        if all(p is None for p in lobbies[current_lobby]["players"]):
            del lobbies[current_lobby]
            print(f"Lobby {current_lobby} closed (All players crashed/left).")
    # ==================================================

    conn.close()

print("Server Running... Waiting for players to connect.")
while True:
    conn, addr = s.accept()
    threading.Thread(target=threaded_client, args=(conn,), daemon=True).start()