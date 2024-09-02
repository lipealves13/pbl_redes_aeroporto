import socket
import pickle
from Models.Voo import Voo
from Models.Vaga import Vaga
from Models.Passageiro import Passageiro
from Models.Passagem import Passagem

voos = []

def mock_voos():
    voo1 = Voo(1, "2024-09-15", "Belém", "Fortaleza")
    voo1.adicionar_vaga(Vaga("disponivel", "1A", voo1))
    voo1.adicionar_vaga(Vaga("disponivel", "1B", voo1))
    voos.append(voo1)

    voo2 = Voo(2, "2024-09-16", "Fortaleza", "São Paulo")
    voo2.adicionar_vaga(Vaga("disponivel", "2A", voo2))
    voo2.adicionar_vaga(Vaga("disponivel", "2B", voo2))
    voos.append(voo2)

mock_voos()

def handle_client(client_socket):
    try:
        while True:
            request = client_socket.recv(4096)
            if not request:
                break

            data = pickle.loads(request)
            action = data.get('action')

            if action == 'listar_voos':
                response = [(voo.id_voo, voo.local_saida, voo.local_destino) for voo in voos]
            elif action == 'listar_vagas':
                voo_id = data.get('voo_id')
                voo = next((v for v in voos if v.id_voo == voo_id), None)
                if voo:
                    response = [(vaga.assento, vaga.status) for vaga in voo.listar_vagas_disponiveis()]
                else:
                    response = "Voo não encontrado"
            elif action == 'reservar_vaga':
                voo_id = data.get('voo_id')
                assento = data.get('assento')
                voo = next((v for v in voos if v.id_voo == voo_id), None)
                if voo:
                    vaga = next((v for v in voo.vagas if v.assento == assento), None)
                    if vaga and vaga.reservar():
                        response = f"Assento {assento} reservado com sucesso."
                    else:
                        response = "Assento indisponível ou não encontrado."
                else:
                    response = "Voo não encontrado"
            else:
                response = "Ação inválida"

            client_socket.send(pickle.dumps(response))
    except Exception as e:
        print(f"Erro ao lidar com cliente: {e}")
    finally:
        client_socket.close()

def server(host='localhost', port=8082):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print("Servidor rodando e aguardando conexões...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Conexão estabelecida com {addr}")
        handle_client(client_socket)

server()
