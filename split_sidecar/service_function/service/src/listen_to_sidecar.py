import base64
import json
import socket
import time

import importlib
import app

MY_IP = 'service'
SIDECAR_IP = 'sidecar'
PORT = 1234
BUFF_SIZE = 10 * 1024


def tcp():
    print('listening TCP')
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((MY_IP, PORT))
        s.listen()

        # recieve from sidecar
        while True:
            recieve_data = b''
            client_sock, client_address = s.accept()

            while True:
                _data = client_sock.recv(BUFF_SIZE)

                if not _data:
                    break
                else:
                    recieve_data += _data
            recieve_data = json.loads(recieve_data.decode())
            # print(recieve_data)

            recieve_data = [base64.b64decode(d.encode()) for d in recieve_data]

            # call service function
            importlib.reload(app)
            # print(recieve_data)
            t = time.time()
            recieve_data = app.function(recieve_data)
            print('service time [s]:'.ljust(20), time.time() - t)
            # print(recieve_data)

            # send back to sidecar
            recieve_data = [base64.b64encode(d).decode('utf-8')
                            for d in recieve_data]
            client_sock.sendall(json.dumps(recieve_data).encode())
            client_sock.close()


SEGMENT_SIZE = 1024
END_MARKER = b'__end__'


def recv_data_udp(s):
    recieve_data = b''
    while True:
        seg, addr = s.recvfrom(BUFF_SIZE)

        if seg == END_MARKER:
            break
        recieve_data += seg
    recieve_data = json.loads(recieve_data.decode())
    # print(recieve_data)
    recieve_data = [base64.b64decode(d.encode()) for d in recieve_data]
    return recieve_data


def udp():
    print('listening UDP')
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.bind((MY_IP, PORT))

            # recieve from sidecar
            recieve_data = recv_data_udp(s)
            print('recieved')

            # call service function
            importlib.reload(app)
            # print(recieve_data)
            t = time.time()
            recieve_data = app.function(recieve_data)
            print('service time [s]:'.ljust(20), time.time() - t)
            # print(recieve_data)

            # send back to sidecar
            send_data = [base64.b64encode(d).decode('utf-8')
                         for d in recieve_data]
            send_data = json.dumps(send_data).encode()
            num_seg = (len(send_data) + SEGMENT_SIZE - 1) // SEGMENT_SIZE
            send_data = [
                send_data[i*SEGMENT_SIZE:(i+1)*SEGMENT_SIZE] for i in range(num_seg)]
            for seg in send_data:
                s.sendto(seg, (SIDECAR_IP, PORT))
                time.sleep(0.001)
            s.sendto(END_MARKER, (SIDECAR_IP, PORT))
            s.close()


if __name__ == '__main__':
    tcp()
    # udp()
