import socket
import argparse

def main():
    parser = argparse.ArgumentParser(description="Cliente para Chatbot JDM")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Dirección IP del servidor")
    parser.add_argument("--port", type=int, default=5555, help="Puerto del servidor")
    args = parser.parse_args()

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((args.host, args.port))
    print(client.recv(1024).decode())

    while True:
        option = input("Selecciona una opción: ")
        client.send(option.encode())
        response = client.recv(1024).decode()
        print(f"Respuesta del servidor: {response}")
        if option == "0":
            break

    client.close()

if __name__ == "__main__":
    main()