import base64
import json
import socket
import time

import importlib
import app

SIDECAR_IP = 'sidecar'
MY_IP = 'service'
PORT = 1234
RECIEVE_SIZE = 1024


print('listening')
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((MY_IP, PORT))
    s.listen()

    # recieve from sidecar
    while True:
        recieve_message = b''
        client_sock, client_address = s.accept()

        # LISTENING
        while True:
            _message = client_sock.recv(RECIEVE_SIZE)

            if not _message:
                break
            else:
                recieve_message += _message
        recieve_message = json.loads(recieve_message.decode())
        print(recieve_message)

        data_list = []
        for name in recieve_message:
            with open('/data/' + name, 'rb') as f:
                data_list.append(f.read())

        # CALL SERVICE FUNCTION
        print('call service function')
        importlib.reload(app)
        t = time.time()
        processed_data = app.function(data_list)
        print('service time:'.ljust(20), time.time() - t)

        if type(processed_data) is type([]):
            processed_data = processed_data[0]
        processed_data = bytes(processed_data)

        # SEND BACK TO SIDECAR
        send_message = ['data']
        with open('/data/' + send_message[0], 'wb') as f:
            f.write(processed_data)

        # send back to sidecar
        client_sock.sendall(json.dumps(send_message).encode())
        client_sock.close()
