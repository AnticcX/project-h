import socket
import sys
import errno
import threading
import pickle
import time

from Player import Player

HEADER_LENGTH = 10

IP = "192.168.0.165"
PORT = 15132

class Network:
    def __init__(self, player: Player) -> None:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((IP, PORT))
        self.socket.setblocking(False)
    
        self.packet = {None: None}
        self.received_packet = None
        
        self.player = player
        self.running = True
        threading.Thread(target=self.listen).start()
    
    def update_packet(self) -> None:
        self.packet = {
            "player_id": self.player.id,
            "player_coords": self.player.coords,
            "player_rotation": self.player.rotation
        }
        
    def send_packet(self) -> None:
        try:
            packet = pickle.dumps(self.packet)
            packet_header = f"{len(packet):<{HEADER_LENGTH}}".encode()
            self.socket.send(packet_header + packet)
        except BlockingIOError:
            pass
        
    def listen(self):
        print(f"Connected to {IP}:{PORT}")
        while self.running:
            time.sleep(0.005)
            self.update_packet()
            self.send_packet()
            try:
                while True:
                    packet_header = self.socket.recv(HEADER_LENGTH)
                    packet_length = int(packet_header.decode().strip())
                    packet = pickle.loads(self.socket.recv(packet_length))
                    self.received_packet = packet
            except IOError as e:
                if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                    print('Reading error: {}'.format(str(e)))
                    print(f"Disconnected from server")
                    sys.exit()
                continue
            except Exception as e:
                print('Reading error: {}'.format(str(e)))
                print(f"Disconnected from server")
                sys.exit()
        else:
            print(f"Disconnected from server")
            