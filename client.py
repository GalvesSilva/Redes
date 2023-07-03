import socket
import time
import json
import os
import threading
from collections import Counter

class Client:
    def __init__(self):
        self.tracker_address = ('192.168.0.226', 5000)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(self.tracker_address)
        self.listening_port = 6000
        self.server = None
        self.files_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files')

    
    def get_own_files(self):
        files = [file for file in os.listdir(self.files_directory)]
        return files

    def set_data(self):
        data = {
            "port": self.listening_port,
            "files": self.get_own_files(),
        }
        return json.dumps(data)

    def send_info(self):
        info = self.set_data()
        self.client_socket.send(info.encode())

    def get_clients_information(self):
        self.client_socket.send("get_clients".encode())
        data = self.client_socket.recv(1024).decode()
        
        try:
            return json.loads(data)
        except json.JSONDecodeError:
            print("Erro ao decodificar dados JSON do servidor")
            return []

    def find_rarest_file(self):
        clients = self.get_clients_information()
        all_files = [file for client in clients for file in client['files']]
        file_counts = Counter(all_files)
        least_common_file = min(file_counts, key=file_counts.get)
        return least_common_file

    def get_peer_wiht_rarest_file(self):
        own_files = self.get_own_files()
        least_common_file = self.find_rarest_file()

        clients = self.get_clients_information()
        rarest_clients = []
        rarest_clients_port = []

        for client in clients:
            if least_common_file in client['files']:
                rarest_clients.append(client['address'])
                rarest_clients_port.append(client['port'])
                break

        if least_common_file not in own_files:
            if rarest_clients:
                client_address = rarest_clients[0][0]
                client_port = rarest_clients_port[0]
                threading.Thread(target=self.get_rarest_file, args=(client_address, client_port)).start()
            else:
                print("Nenhum cliente tem o arquivo mais raro.")
    
    def get_rarest_file(self, client_address, client_port):
        file_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            file_socket.connect((client_address, client_port))
            file_socket.send("get_file".encode())
            file_data = file_socket.recv(1024)
            filename = os.path.basename(self.find_rarest_file())
            file_path = os.path.join(self.files_directory, filename)
            with open(file_path, 'wb') as file:
                file.write(file_data)
            print(f"Obteve o arquivo mais rado do: {client_address}:{client_port}")
        except Exception as e:
            print(f"Falhou em obter o arquivo mias raro do: {client_address}:{client_port}. Error: {str(e)}")
        finally:
            file_socket.close()
    
    def handle_request(self, client_socket):
        request = client_socket.recv(1024).decode()
        if request == "get_file":
            rarest_file = self.find_rarest_file()
            if rarest_file in self.get_own_files():
                file_path = os.path.join(self.files_directory, rarest_file)
                with open(file_path, 'rb') as file:
                    file_data = file.read()
                client_socket.send(file_data)
            else:
                client_socket.send("Arquivo não encontrado".encode())
        else:
            client_socket.send("Request desconhecido".encode())
        client_socket.close()

    def start_peer_con(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((socket.gethostname(), self.listening_port))
        self.server.listen(5)

        while True:
            client_socket, address = self.server.accept()
            client_thread = threading.Thread(target=self.handle_request, args=(client_socket,))
            client_thread.start()

    def print_connected_clients(self):
        clients = self.get_clients_information()
        print("Peers Conectados:")
        for client in clients:
            files = ", ".join([os.path.basename(file) for file in client['files']])
            print(f"Address: {client['address']}, Port: {client['port']}, Files: {files}")

    def start(self):
        threading.Thread(target=self.start_peer_con).start()
        self.send_info()
        self.print_connected_clients()
        time_passed = 0

        while True:
            time.sleep(10)
            self.send_info()
            self.print_connected_clients()
            self.get_peer_wiht_rarest_file()
            time_passed += 10;

            if(time_passed == 180):
                self.send_info()
                time_passed = 0

if __name__ == '__main__':
    client = Client()
    client.start()
