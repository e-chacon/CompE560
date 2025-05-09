import socket
import threading
import base64
from crypto_utils import generate_aes_key, encrypt_with_rsa, decrypt_with_aes, encrypt_with_aes
from datetime import datetime

clients = {}
client_keys = {}

def handle_messages(sock):
    """
    Handles incoming messages and key exchanges.
    Example:
        >>> handle_messages(sock)  # This will start listening for messages

    Args:
        sock (socket.socket): The socket to receive messages from.
    returns:
        None
    raises:
        None

    1. Receives messages from the socket.
    2. If the message is from a known client, decrypts it and broadcasts it to other clients. 
    3. If the message is from a new client, exchanges keys and stores the client's address and AES key.
    4. Prints the received messages with timestamps.
    5. Exits if decryption fails.
    6. Handles exceptions during decryption.
    7. Uses a while loop to continuously listen for messages.
    8. Uses a try-except block to handle decryption errors.
    9. Uses a for loop to broadcast messages to other clients.
    """
    while True:
        data, addr = sock.recvfrom(4096)
        if addr in clients:
            aes_key = clients[addr]
            # Broadcast the encrypted message to other clients
            try:
                decrypted_message = decrypt_with_aes(aes_key, data.decode())
                print(f"Received from {addr}: {decrypted_message}", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            except Exception as e:
                print(f"Decryption failed for {addr}: {e}")
                continue

            for client_addr, key in clients.items():
                if client_addr != addr:
                    encrypted_message = encrypt_with_aes(key, decrypted_message)
                    sock.sendto(encrypted_message.encode(), client_addr)
        else:
            # First message is assumed to be client's RSA public key
            rsa_pub_key = base64.b64decode(data)
            aes_key = generate_aes_key()
            encrypted_key = encrypt_with_rsa(rsa_pub_key, aes_key)
            sock.sendto(base64.b64encode(encrypted_key), addr)
            clients[addr] = aes_key
            client_keys[addr] = rsa_pub_key
            print(f"Key exchanged with {addr}")

def main():
    """
    Main function to set up the server.
    Example:
        >>> main()  # This will start the server

    Args:
        None
    returns:
        None
    raises:
        None

    1. Creates a UDP socket.
    2. Binds the socket to localhost and port 12345.
    3. Starts listening for incoming messages.
    4. Handles incoming messages and key exchanges.
    5. Prints the received messages with timestamps.
    6. Exits if decryption fails.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("localhost", 12345))
    print("Server started on port 12345")
    handle_messages(sock)

if __name__ == "__main__":
    main()
