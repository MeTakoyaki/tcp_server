import socket
import threading
import logging
import signal
import sys
from config import IP, PORT, MAX_CONNECTIONS, BUFFER_SIZE

# Konfigurasi logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("server.log"), # simpan log ke file
        logging.StreamHandler() # tampilkan log di terminal
    ]
)

def handle_client(client_socket, address):
    '''Fungsi untuk menangani komunikasi dengan klien'''
    logging.info(f"[*] Connection established from {address[0]}:{address[1]}")
    
    try:
        with client_socket as sock :
            request = sock.recv(1024)
            if request :
                 logging.info(f"[*] Received from {address[0]}:{request.decode('utf-8')}")
                 sock.send(b"ACK")
            else :
                logging.warning(f"[!] Empty request received from {address[0]}")
    except Exception as e :
        logging.error(f"[!] Error handling client {address[0]}:{e}")

def main():
    """Fungsi utama untuk menjalankan server"""
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    
    try:
        server.bind((IP, PORT))
        server.listen(MAX_CONNECTIONS)
        logging.info(f'[*] Listening on {IP}:{PORT}')

        # menangani shutdown dengan baik
        def signal_handler(sig, frame)
        logging.info("shutting down server...")
        server.close()
        sys.exit(0)

        signal.signal(signal.SIGINT, signal_handler) # menangani CTRL + C

        while True:
            client, address = server.accept()
            client_handler = threading.Thread (target=handle_client, args=(client, address), daemon=True)
            client_handler.start()
    except Exception as e:
        logging.error(f"[!] Server error : {e}")
    finally:
        server.close()
    
if __name__ == '__main__':
    main()