from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import base64

# --- RSA Operations ---
def generate_rsa_keypair():
    """
    Generates a new RSA key pair.
    Args:
        None
    Returns:
        tuple: A tuple containing the private and public keys in bytes.
    Raises:
        None
    """
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key

def encrypt_with_rsa(public_key_bytes, message_bytes):
    """
    Encrypts a message using RSA public key.
    Args:
        public_key_bytes (bytes): The public key in bytes.
        message_bytes (bytes): The message to encrypt in bytes.
    Returns:
        bytes: The encrypted message in bytes.
    Raises:
        None
    """

    pub_key = RSA.import_key(public_key_bytes)
    cipher_rsa = PKCS1_OAEP.new(pub_key)
    return cipher_rsa.encrypt(message_bytes)

def decrypt_with_rsa(private_key_bytes, encrypted_bytes):
    """
    Decrypts a message using RSA private key.
    Args:
        private_key_bytes (bytes): The private key in bytes.
        encrypted_bytes (bytes): The encrypted message in bytes.
    Returns:
        bytes: The decrypted message in bytes.
    Raises:
        None
    """
    priv_key = RSA.import_key(private_key_bytes)
    cipher_rsa = PKCS1_OAEP.new(priv_key)
    return cipher_rsa.decrypt(encrypted_bytes)

# --- AES Operations ---
def generate_aes_key():
    """
    Generates a random AES key.
    Args:
        None
    Returns:
        bytes: A random AES key in bytes.
    Raises:
        None
    """
    return get_random_bytes(16) # 128-bit key

def encrypt_with_aes(aes_key, plaintext):
    """
    Encrypts a plaintext message using AES encryption.
    Args:
        aes_key (bytes): The AES key in bytes.
        plaintext (str): The plaintext message to encrypt.
    Returns:
        str: The base64 encoded ciphertext.
    Raises:
        None
    """
    iv = get_random_bytes(16)
    cipher = AES.new(aes_key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(plaintext.encode(), AES.block_size))
    return base64.b64encode(iv + ciphertext).decode()

def decrypt_with_aes(aes_key, b64_ciphertext):
    """
    Decrypts a base64 encoded ciphertext using AES decryption.
    Args:
        aes_key (bytes): The AES key in bytes.
        b64_ciphertext (str): The base64 encoded ciphertext to decrypt.
    Returns:
        str: The decrypted plaintext message.
    Raises:
        None
    """
    raw = base64.b64decode(b64_ciphertext)
    iv = raw[:16]
    ciphertext = raw[16:]
    cipher = AES.new(aes_key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(ciphertext), AES.block_size).decode()
