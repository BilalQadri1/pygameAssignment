import socket
import pickle
import struct

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "3.99.154.115" # Put your AWS IP here! 
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def connect(self):
        try:
            self.client.connect(self.addr)
            # Read the welcome message from the server
            return self._recv_data()
        except Exception as e:
            print(f"Connection failed: {e}")
            return None

    def send(self, data):
        try:
            # 1. Pack the data
            packed_data = pickle.dumps(data)
            # 2. Pack the length of the data into a 4-byte header ('I' = unsigned integer)
            header = struct.pack('I', len(packed_data))
            # 3. Send header + data
            self.client.sendall(header + packed_data)
            
            # Wait for the server's clean response
            return self._recv_data()
            
        except Exception as e:
            if self.p is not None:
                print(f"Server disconnected.")
                self.p = None
            return "SERVER_DEAD"

    def _recv_data(self):
        # Internal helper to safely read the exact packet size
        try:
            # Read the 4-byte header
            raw_msglen = self._recvall(4)
            if not raw_msglen:
                return None
            msglen = struct.unpack('I', raw_msglen)[0]
            
            # Read exactly 'msglen' bytes
            raw_data = self._recvall(msglen)
            if not raw_data:
                return None
            return pickle.loads(raw_data)
        except Exception as e:
            return None

    def _recvall(self, n):
        # Helper function to ensure we receive ALL expected bytes
        data = bytearray()
        while len(data) < n:
            packet = self.client.recv(n - len(data))
            if not packet:
                return None
            data.extend(packet)
        return data