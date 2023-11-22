import socket
import select
import pickle
import time

from world.world import World

HEADER_LENGTH = 10

IP = "192.168.0.165"
PORT = 15132

class Server:
    def __init__(self) -> None:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((IP, PORT))
        
        self.sockets_list = [self.socket]
        self.clients = {}
        self.client_datas = {}
        
        self.world = World()
        
    def receive_packet(self, client_socket: socket.socket):
        try:
            packet_header = client_socket.recv(HEADER_LENGTH)
            if not len(packet_header):return False
            
            packet_length = int(packet_header.decode().strip())
            return {'header': packet_header, 'data': pickle.loads(client_socket.recv(packet_length))}
        except: return False
    
    def send_packet(self, client_socket: socket.socket, packet: object) -> None:
        try:
            
            packet = pickle.dumps(packet)
            packet_header = f"{len(packet):<{HEADER_LENGTH}}".encode()
            client_socket.send(packet_header + packet)
            
        except BlockingIOError: pass
        except ConnectionResetError: pass
        
    def listen(self) -> None:
        self.socket.listen()
        print(f'Listening for connections on {IP}:{PORT}...')
        while True:
            read_sockets, _, exception_sockets = select.select(self.sockets_list, [], self.sockets_list)
            
            for notified_socket in read_sockets:
                if notified_socket == self.socket:
                    client_socket, client_address = self.socket.accept()
                    
                    packet = self.receive_packet(client_socket)
                    if packet is False: continue
                    
                    self.sockets_list.append(client_socket) 
                    
                    data = packet["data"]
                    self.client_datas[data["player_id"]] = data 
                    self.clients[client_socket] = packet

                    self.send_packet(client_socket, {"world": self.world})
                    time.sleep(0.0055)
                    print(f'{data["player_id"]} ({client_address[0]}:{client_address[1]}) has connected to the server')
                else:
                    try: 
                        packet = self.receive_packet(notified_socket)
                        data = packet["data"]
                        self.client_datas[data["player_id"]] = data
                    except TypeError: pass
                    
                    data = self.clients[notified_socket]['data']
                    player_id = data["player_id"]
                    
                    if packet is False:
                        print(f'{player_id} has disconnected from the server')
                        
                        self.sockets_list.remove(notified_socket)
                        
                        try:
                            del self.client_datas[player_id]
                            del self.clients[notified_socket]
                        except TypeError: pass
                        continue 
                    
                    for client_socket in self.clients:
                        self.send_packet(client_socket, self.client_datas)

            
            for notified_socket in exception_sockets:
                self.sockets_list.remove(notified_socket)
                
                data = self.clients[notified_socket]['data']
                del self.client_datas[data['player_id']]
                del self.clients[notified_socket]
            

if __name__ == "__main__": 
    server = Server() 
    server.listen()