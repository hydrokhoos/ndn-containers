import json
import base64
import socket
import time
import os
from tqdm import tqdm


MY_IP = 'sidecar'
SERVICE_IP = 'service'
PORT = 1234
BUFF_SIZE = 10 * 1024

# send_data = [b'test1', b'test2']

# with open('/src/img1.png', 'rb') as f:
#     data1 = f.read()
# with open('/src/img2.png', 'rb') as f:
#     data2 = f.read()
# send_data = [data1, data2]

t = time.time()
data_size = 30 * 1024 * 1024
data1 = os.urandom(data_size)
data2 = os.urandom(data_size)
send_data = [data1, data2]
print('gen data size [KB]:'.ljust(20), data_size//(8 * 1024))
print('gen data time [s]:'.ljust(20), time.time() - t)


def tcp():
    print('socket start TCP')
    t = time.time()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((SERVICE_IP, PORT))

        # send to service
        if send_data:
            _data = json.dumps([base64.b64encode(d).decode('utf-8')
                                for d in send_data]).encode()
            print('sending')
            s.sendall(_data)
            s.shutdown(1)
            print('sent')

        # recieve from service
        print('wait for data')
        recieve_data = b''
        while True:
            _data = s.recv(BUFF_SIZE)
            if not _data:
                break
            else:
                recieve_data += _data
        recieve_data = json.loads(recieve_data.decode())
        recieve_data = [base64.b64decode(d.encode()) for d in recieve_data]
        print('recieved')

    print('socket time [s]:'.ljust(20), time.time() - t)

    # print(f'send_data: {send_data}')
    # print(f'recieve_data: {recieve_data}')
    if all([send_data[i] == recieve_data[i] for i in range(len(send_data))]):
        print('data check OK')


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
    print('socket start UDP')
    t = time.time()
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        # send to service
        if send_data:
            _data = json.dumps([base64.b64encode(d).decode('utf-8')
                                for d in send_data]).encode()

            num_seg = (len(_data) + SEGMENT_SIZE - 1) // SEGMENT_SIZE
            _data_list = [_data[i*SEGMENT_SIZE:(i+1)*SEGMENT_SIZE]
                          for i in range(num_seg)]

            print('sending')
            for d in tqdm(_data_list):
                s.sendto(d, (SERVICE_IP, PORT))
                time.sleep(0.001)
            s.sendto(END_MARKER, (SERVICE_IP, PORT))
            s.close()
            print('sent')

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        # recieve from service
        s.bind((MY_IP, PORT))
        print('wait for data')
        recieve_data = recv_data_udp(s)
        print('recieved')

        print('socket time [s]:'.ljust(20), time.time() - t)

        # print(f'send_data: {send_data}')
        # print(f'recieve_data: {recieve_data}')
        if all([send_data[i] == recieve_data[i] for i in range(len(send_data))]):
            print('data check OK')


if __name__ == '__main__':
    tcp()
    # udp()
