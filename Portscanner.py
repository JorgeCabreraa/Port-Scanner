import socket
import argparse
import sys
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

def scan_port(ip, port):
    """Intenta conectarse a un puerto específico y devuelve el resultado."""
    try:
        # Creamos el socket con un timeout corto para mayor velocidad
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1.0)
            result = sock.connect_ex((ip, port))
            if result == 0:
                print(f"[+] Puerto abierto: {port}")
    except Exception:
        pass # Ignoramos errores de conexión individuales

def main():
    # Configuración de argumentos de línea de comandos
    parser = argparse.ArgumentParser(description="Escáner de puertos rápido en Python")
    parser.add_argument("target", help="Dirección IP o Host a escanear")
    parser.add_argument("-p", "--ports", type=int, nargs=2, default=[1, 1024],
                        help="Rango de puertos (ejemplo: 20 80). Por defecto: 1-1024")
    parser.add_argument("-t", "--threads", type=int, default=100,
                        help="Número de hilos a usar. Por defecto: 100")

    args = parser.parse_args()
    target_ip = socket.gethostbyname(args.target)
    start_port, end_port = args.ports

    print("-" * 50)
    print(f"Escaneando objetivo: {target_ip}")
    print(f"Inicio: {datetime.now()}")
    print("-" * 50)

    # Uso de ThreadPoolExecutor para gestionar el paralelismo
    try:
        with ThreadPoolExecutor(max_workers=args.threads) as executor:
            # Creamos una lista de tareas para el rango de puertos solicitado
            for port in range(start_port, end_port + 1):
                executor.submit(scan_port, target_ip, port)
                
    except KeyboardInterrupt:
        print("\n[!] Saliendo... Escaneo interrumpido.")
        sys.exit()

    print("-" * 50)
    print(f"Escaneo finalizado en: {datetime.now()}")

if __name__ == "__main__":
    main()
