import threading, random, time 

class Thread:
    def __init__(self) -> None:
        self.queue: dict = {}
        self.running: list = [] 
        
    def generate_uid(self) -> str:
        uid = None
        while uid in self.queue or uid is None: uid = "%032x" % random.getrandbits(128)
        return uid
    
    def add_queue(self, func, args: tuple = ()) -> str:
        uid = self.generate_uid()
        self.queue[uid] = [func, args]
        return uid
        
    def remove_queue(self, uid) -> bool:
        if not uid in self.queue: return False
        del self.queue[uid] 
        return True
        
    def run_queue(self) -> None:
        for uid in self.queue.copy():
            if len(self.running) >= 6: return
            thread = threading.Thread(target=self.run_thread, args=[uid])
            thread.start()
        
    def run_thread(self, uid: str) -> None:
        func, args = self.queue[uid]
        
        self.running.append(uid)
        self.remove_queue(uid)
        
        func(*args)
        
        self.running.remove(uid)