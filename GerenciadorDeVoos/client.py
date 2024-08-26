import socket
def client(host = 'localhost', port=8082): 
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    server_address = (host, port) 
    print ("Conectando em: %s port %s" % server_address) 
    sock.connect(server_address) 
    try: 
        message = "Mensagem de teste." 
        print ("Enviando: %s" % message) 
        sock.sendall(message.encode('utf-8')) 
        amount_received = 0 
        amount_expected = len(message) 
        while amount_received < amount_expected: 
            data = sock.recv(16) 
            amount_received += len(data) 
            print ("Recebido: %s" % data) 
    except socket.error as e: 
        print ("Erro de Socket: %s" %str(e)) 
    except Exception as e: 
        print ("Erro desconhecido: %s" %str(e)) 
    finally: 
        print ("Fechando conexão com o servidor") 
        sock.close() 

client()