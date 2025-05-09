import socket
import threading
import base64
from crypto_utils import (
    generate_rsa_keypair, decrypt_with_rsa,
    encrypt_with_aes, decrypt_with_aes
)
from datetime import datetime
aes_key = None
def receive_messages(sock, private_key):
    """
    Receives messages from the server and decrypts them.
    Example:
        >>> receive_messages(sock, private_key)  # This will start listening for messages

    Args:
        sock (socket.socket): The socket to receive messages from.
        private_key (bytes): The private RSA key for decryption.
    returns:
        None
    raises:
        None

    1. Receives data from the socket.
    2. If the AES key is not set, decrypts the received data using RSA.
    3. If the AES key is set, decrypts the received data using AES.
    4. If the decrypted data contains "||", splits it into sender and message.
    5. Prints the sender and message with a timestamp.
    6. If decryption fails, prints an error message and exits.
    7. Uses a while loop to continuously listen for messages.
    8. Uses a try-except block to handle decryption errors.
    """
    global aes_key
    while True:
        data, _ = sock.recvfrom(4096)  # Receive data from the socket
        if aes_key is None:
            encrypted_key = base64.b64decode(data)
            aes_key = decrypt_with_rsa(private_key, encrypted_key)
            print("Received and decrypted AES key.")
        else:
            try:
                decrypted = decrypt_with_aes(aes_key, data.decode())
                if "||" in decrypted:
                    sender, message = decrypted.split("||", 1)
                    print(f"\r{sender}: {message}\t{datetime.now().strftime('%H:%M:%S')}")
                    print(">> ", end="", flush=True)
                else:
                    print(f"Received message: {decrypted}\t{datetime.now().strftime('%H:%M:%S')}")
            except Exception as e:
                print("Decryption failed:", e)
                break  # Exit if decryption fails, possibly due to key mismatch or other issues
def main():
    """
    Main function to set up the client.
    Example:
        >>> main()  # This will start the client
        
    Args:
        None
    returns:
        None
    raises:
        None

    1. Creates a UDP socket.
    2. Binds the socket to localhost and port 12345.
    3. Generates RSA keys and sends the public key to the server.
    4. Starts a thread to receive messages from the server.
    5. Waits for the AES key to be received.
    6. Asks the user for their name.
    7. Continuously listens for user input and sends messages to the server.
    8. Uses a while loop to continuously listen for messages.
    9. Uses a try-except block to handle decryption errors.
    """
    global aes_key
    server_addr = ("localhost", 12345)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Generate RSA keys and send public key
    private_key, public_key = generate_rsa_keypair()
    sock.sendto(base64.b64encode(public_key), server_addr)

    # Start thread to receive messages
    threading.Thread(target=receive_messages, args=(sock, private_key), daemon=True).start()

     # Wait for AES key before asking for name
    while aes_key is None:
        pass

    # Ask for client name
    name = input("Enter your name: ").strip()
    while not name:
        name = input("Name cannot be empty. Please enter your name: ").strip()

    while True:
        msg = input(">> ").strip()
        while not msg:
            msg = input("Message cannot be empty. Please enter a message: ").strip()
        if aes_key:
            payload = f"{name}||{msg}"
            encrypted = encrypt_with_aes(aes_key, payload)
            sock.sendto(encrypted.encode(), server_addr)
        else:
            print("Waiting for key exchange to complete...")
if __name__ == "__main__":
    main()
