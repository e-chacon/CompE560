Usage
=====

.. autofunction:: server.main
Server.main
-----------------
Starts the UDP server and listens for incoming messages. It handles
the incoming messages and sends responses back to the client.
.. py:function:: server.main()
    :returns: None
    :rtype: NoneType

    This function initializes the server, binds it to the specified address and port,
    and starts listening for incoming messages. It handles incoming messages in a loop
    and sends responses back to the client.
    It also handles any exceptions that may occur during the process.
.. autofunction:: server.handle_messages
Server.handle_messages
-----------------
Handles incoming messages from the client. It processes the message and sends a response back.
.. py:function:: server.handle_messages()
    :param data: The incoming message data.
    :type data: bytes
    :param addr: The address of the client that sent the message.
    :type addr: tuple
    :returns: None
    :rtype: NoneType

    This function processes the incoming message and sends a response back to the client.
    It also handles any exceptions that may occur during the process.

.. autofunction:: client.main
Client.main
-----------------
Starts the UDP client and sends messages to the server. It also receives responses from the server.
.. py:function:: client.main()
    :returns: None
    :rtype: NoneType

    This function initializes the client, connects to the server, and starts sending messages.
    It also receives responses from the server and handles any exceptions that may occur during the process.

.. autofunction:: client.receive_messages
Client.receive_messages
-----------------
Receives messages from the server. It processes the received messages and handles any exceptions that may occur.
.. py:function:: client.receive_messages()
    :returns: None
    :rtype: NoneType

    This function receives messages from the server and processes them.
    It also handles any exceptions that may occur during the process.