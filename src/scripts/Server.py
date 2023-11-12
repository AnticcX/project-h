import sys, socket, selectors, types, threading, time

class Server:
    def __init__(self) -> None:
        self.IP = "192.168.0.165"
        self.PORT = 15632
        
        self.sel = selectors.DefaultSelector()
        self.lsock = None
        
        
    def start(self) -> None:
        self.lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.lsock.bind((self.IP, self.PORT))
        self.lsock.listen() 
        
        self.lsock.setblocking(False)
        self.sel.register(self.lsock, selectors.EVENT_READ, data=None)
        
        print(f"Listening on {(self.IP, self.PORT)}")
        self.event_loop()
    
    def event_loop(self) -> None:
        try:
            while True:
                events = self.sel.select(timeout=None)
                for key, mask in events:
                    if key.data is None:
                        self.accept_wrapper(key.fileobj)
                    else:
                        self.service_connection(key, mask)
        except KeyboardInterrupt: pass
        finally: self.sel.close()
        
    def accept_wrapper(self, socket) -> None:
        conn, addr = socket.accept()
        print(f"Connected from {addr}")
        
        conn.setblocking(False)
        data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        self.sel.register(conn, events, data=data)
        
    def service_connection(self, key, mask) -> None:
        socket = key.fileobj
        data = key.data
        if mask & selectors.EVENT_READ:
            recv_data = socket.recv(1024)
            if recv_data:
                data.outb += recv_data
            else:
                print(f"Closing connection to {data.addr}")
                self.sel.unregister(socket)
                socket.close()
        if mask & selectors.EVENT_WRITE:
            if data.outb:
                print(f"Echoing {data.outb!r} to {data.addr}")
                sent = socket.send(data.oub)
                data.outb = data.outb[sent:]
        
        
class Client:
    def __init__(self) -> None:
        self.IP = "192.168.0.165"
        self.PORT = 15632
        
        self.sel = selectors.DefaultSelector()
        self.messages = [b"Message 1 from client.", b"Message 2 from client."]
    
    def connect(self, host, port, num_conns) -> None:
        server_addr = (host, port)
        for i in range(num_conns):
            connid = i + 1
            print(f"Starting connection {connid} to {server_addr}")
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setblocking(False)
            sock.connect_ex(server_addr)
            events = selectors.EVENT_READ | selectors.EVENT_WRITE
            data = types.SimpleNamespace(
                connid=connid,
                msg_total=sum(len(m) for m in self.messages),
                recv_total=0,
                messages=self.messages.copy(),
                outb=b"",
            )
            self.sel.register(sock, events, data=data)
        self.event_loop()
    
    def event_loop(self) -> None:
        try:
            while True:
                events = self.sel.select(timeout=None)
                for key, mask in events:
                    if key.data is None:
                        self.accept_wrapper(key.fileobj)
                    else:
                        self.service_connection(key, mask)
        except KeyboardInterrupt: pass
        finally: self.sel.close()
    
    def service_connection(self, key, mask):
        socket = key.fileobj
        data = key.data
        if mask & selectors.EVENT_READ:
            recv_data = socket.recv(1024)  # Should be ready to read
            if recv_data:
                print(f"Received {recv_data!r} from connection {data.connid}")
                data.recv_total += len(recv_data)
            if not recv_data or data.recv_total == data.msg_total:
                print(f"Closing connection {data.connid}")
                self.sel.unregister(socket)
                socket.close()
        if mask & selectors.EVENT_WRITE:
            if not data.outb and data.messages:
                data.outb = data.messages.pop(0)
            if data.outb:
                print(f"Sending {data.outb!r} to connection {data.connid}")
                sent = socket.send(data.outb)  # Should be ready to write
                data.outb = data.outb[sent:]
        
server = Server()
threading.Thread(target=server.start).start()

time.sleep(1)
client = Client() 
client.connect(client.IP, client.PORT, 2)