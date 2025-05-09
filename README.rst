README 
======

Instructions
In order to implement the source code, multiple terminals need to be used.

One terminal will run the 'server.py' code and at least 2 other terminals will run the 'client.py' code.
The clients will automatically create their RSA public/private key pairs and send them to the server.
The server will then assign each client their own specific AES key and encrypt it with their respective RSA public keys before sending them their AES keys.
The AES keys are received by the clients and decrypted with their RSA private keys.
From there all subsequent messages from the clients to the server will be encrypted with an AES key specific to each client.
The server will use each specific AES key to decrypt the messages of each clientconnected to those specific AES keys.
Summary of Choices
I prodominently used the sample code provided because it was a nearly complete implementation of the requisite code for this assignment. After reviewing all the functions and facets of the provided code, I concluded that using the code will be the simplest and most efficient method of message encryption. The only thing I had to incorporate to achieve functionality of the chat system was the AES key decryption of messages from clients and the re-encryption of messages when they're broadcast to other clients.

Assumptions of Limitations
Upon asking ChatGPT what some limitations could be of this design could be, I found that there are many limitations and concerns for this code.

Security Limitations
RSA public keys aren't authenticated (man-in-the-middle)
Message integrity isn't check for (could be tampered with)
AES key reuse (reusing the same key per client can be a weakness)
UDP is connectionless and unreliable
Design Limitations
Single-Theaded Server
No disconnect/ timeout handling
No message framing/ size handling
No delivery feedback