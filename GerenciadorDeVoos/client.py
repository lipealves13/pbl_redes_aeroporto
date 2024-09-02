import socket
import pickle

def client(host='localhost', port=8082):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))

    try:
        while True:
            print("\nEscolha uma ação:")
            print("1. Listar voos")
            print("2. Listar vagas de um voo")
            print("3. Reservar uma vaga")
            print("4. Sair")
            escolha = input("Digite o número da ação desejada: ")

            if escolha == '1':
                request = {'action': 'listar_voos'}
                sock.send(pickle.dumps(request))
                response = pickle.loads(sock.recv(4096))
                print("Voos disponíveis:", response)

            elif escolha == '2':
                voo_id = int(input("Digite o ID do voo: "))
                request = {'action': 'listar_vagas', 'voo_id': voo_id}
                sock.send(pickle.dumps(request))
                response = pickle.loads(sock.recv(4096))
                print(f"Vagas disponíveis no voo {voo_id}:", response)

            elif escolha == '3':
                voo_id = int(input("Digite o ID do voo: "))
                assento = input("Digite o número do assento: ")
                request = {'action': 'reservar_vaga', 'voo_id': voo_id, 'assento': assento}
                sock.send(pickle.dumps(request))
                response = pickle.loads(sock.recv(4096))
                print(response)

            elif escolha == '4':
                print("Saindo...")
                break

            else:
                print("Escolha inválida. Tente novamente.")
                
    finally:
        sock.close()

client()
