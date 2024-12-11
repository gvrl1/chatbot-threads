import threading
import socket
from tasks import process_jdm_question

# Configuración del servidor
HOST = '0.0.0.0'  # Acepta conexiones desde cualquier interfaz
PORT = 5555       # Puerto del servidor

menu = """
Bienvenido al Chatbot de JDM 🚗
Selecciona una opción:
1. Historia de JDM
2. Modelos icónicos
3. Piezas y modificaciones
4. Eventos y cultura
0. Salir
"""

# Función para manejar la opción 3 usando Celery
def handle_option_3():
    result = process_jdm_question.delay("Detalles de piezas y modificaciones")
    try:
        # Espera a que la tarea se complete con un timeout
        return result.get(timeout=10)
    except Exception as e:
        return f"Error al procesar la tarea: {str(e)}"

# Diccionario que mapea opciones a funciones
options = {
    "0": lambda: "Gracias por usar el Chatbot de JDM. ¡Hasta luego!",
    "1": lambda: "JDM se refiere a autos fabricados exclusivamente para el mercado japonés.",
    "2": lambda: "Modelos icónicos: Nissan Skyline GT-R, Toyota Supra, Mazda RX-7.",
    "3": handle_option_3,
    "4": lambda: "Eventos populares: Tokyo Auto Salon, eventos de drifting en Japón.",
}

# Función para manejar a cada cliente
def handle_client(conn, addr):
    print(f"Conexión nueva desde {addr[0]}:{addr[1]}")
    conn.sendall(menu.encode())  # Envía el menú al cliente

    while True:
        try:
            data = conn.recv(1024)  # Recibe datos del cliente
            if not data:
                print(f"Cliente {addr[0]} desconectado.")
                break

            option = data.decode().strip()
            print(f"Cliente {addr[0]} seleccionó: {option}")

            if option in options:
                if option == "0":
                    response = options[option]()
                    conn.sendall(response.encode())
                    break  # Termina la conexión
                elif option == "3":
                    response = options[option]()  # Procesa la opción 3
                else:
                    response = options[option]()  # Llama a funciones lambda
            else:
                response = "Opción no válida. Por favor selecciona del 0 al 4."

            conn.sendall(response.encode())  # Envía la respuesta al cliente
        except Exception as e:
            print(f"Error con el cliente {addr[0]}: {e}")
            break

    conn.close()
    print(f"Conexión cerrada con {addr[0]}:{addr[1]}")

# Función principal del servidor
def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((HOST, PORT))
        server.listen()
        print(f"Servidor escuchando en {HOST}:{PORT}...")

        while True:
            conn, addr = server.accept()  # Acepta una nueva conexión
            # Crea un nuevo thread para manejar al cliente
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()  # Inicia el thread
            print(f"Thread iniciado para {addr[0]}:{addr[1]}")

if __name__ == "__main__":
    main()