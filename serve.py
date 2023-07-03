import threading
import socket
import json

class TrackerServer:
    def __init__(self):
        self.clients = []
        self.max_clients = 4
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('192.168.0.141', 5000))
        self.server_socket.listen(5)
        self.lock = threading.Lock()

    def handle_peers(self, client_socket, address):
        with self.lock:
            self.clients.append({"address": address,"port": [], "files": []})

        while True:
            try:
                data = client_socket.recv(1024)
                if not data:
                    break

                decoded_data = data.decode()
                if decoded_data == "get_clients":
                    with self.lock:
                        client_info = [{"address": c["address"],"port": c["port"], "files": c["files"]} for c in self.clients]
                        client_socket.send(json.dumps(client_info).encode())
                else:
                    with self.lock:
                        client = next((c for c in self.clients if c["address"] == address), None)
                        if client:
                            client["files"] = json.loads(decoded_data)["files"]
                            client["port"] = json.loads(decoded_data)["port"]

            except:
                break

        with self.lock:
            for client in self.clients:
                if client["address"] == address:
                    self.clients.remove(client)
                    break

        print("Desconectado:",address)
        client_socket.close()

    def start(self):
        print('Servidor Tracker iniciado. Esperando conexões...')

        while True:
            if len(self.clients) < self.max_clients:
                client_socket, address = self.server_socket.accept()
                print("Conectado:",address)
                client_thread = threading.Thread(target=self.handle_peers, args=(client_socket, address))
                client_thread.start()

if __name__ == '__main__':
    server = TrackerServer()
    server.start()
