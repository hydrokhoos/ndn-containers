from ndn.transport.udp_face import UdpFace
from ndn.app import NDNApp
from ndn.encoding import Name
from ndn.encoding import Component
from ndn.encoding.tlv_type import BinaryStr, FormalName
from ndn.types import (InterestCanceled, InterestNack, InterestTimeout,
                       ValidationFailure)
from ndn.app_support.segment_fetcher import segment_fetcher

import threading
import queue
import time
import csv
import subprocess as sp

sp.call(['cp', '/python-ndn/src/ndn/transport/*',
        '/usr/local/lib/python3.8/dist-packages/ndn/transport'])

service_name = '/relay'

SEGMENT_SIZE = 4400
FRESHNESS_PERIOD = 100000

# q_content = queue.Queue()
q_recent_data = queue.Queue()

host = 'udp4://router.test-net'
port = 6363
app = NDNApp(face=UdpFace(host, port))
# app = NDNApp()

q_get = queue.Queue()
q_put = queue.Queue()

logfile = '/src/relay.csv'


def cat_chunks(name: str) -> bytes:
    name = Name.normalize(name)
    save_name = name[1:].replace('/', '-')
    sp.call(['ndncatchunks', name, '>', save_name])
    data = b''
    with open(save_name, 'rb') as f:
        data = f.read()
    return data


def send_interest(queue: queue.Queue, name: FormalName) -> None:
    async def interest_func(name):
        cnt = 0
        data = b''
        timestamps = []
        async for seg in segment_fetcher(app_thread, name, timeout=4000, retry_times=3):
            data += seg
            cnt += 1
            timestamps.append((str(time.time()), 'relay d-in',
                              Name.to_str(name), str(cnt)))
        queue.put(data)
        q_get.put(timestamps)
        app_thread.shutdown()

    if not queue.empty():
        app_thread.shutdown()
        return
    app_thread = NDNApp()
    app_thread.run_forever(after_start=interest_func(name))


def function_relay(data: bytes) -> bytes:
    # just relay
    return data


def save_data(q: queue.Queue, name: str, data: bytes) -> None:
    while not q.empty():
        q.get()
    q.put({'name': name, 'data': data, 'time': time.time()})


def search_data(q: queue.Queue, name: str) -> bytes:
    if q.empty():
        return None
    data = q.get()
    if (time.time() - data['time']) > FRESHNESS_PERIOD:
        return None
    else:
        q.put(data)
        if data['name'] == name:
            return data['data']
        else:
            return None


def parse_intrest(name: FormalName) -> dict:
    # name='/relay/test.jpg/seg=3'
    # --> org='/relay/test.jpg/seg=3', srch='/relay/test.jpg', trm='/test.jpg', seg_no=3
    org = Name.to_str(name)
    if Component.get_type(Name.from_str(org)[-1]) == Component.TYPE_SEGMENT:
        # interest packet has segment number
        seg_no = Component.to_number(Name.from_str(org)[-1])
        srch = org.replace('/seg=' + str(seg_no), '')
    else:
        seg_no = 0
        srch = org
    trm = Name.to_str(srch).replace(service_name + '/', '')

    return {'org': org, 'srch': srch, 'trm': trm, 'num': seg_no}


async def main():
    print(f'My service name: {service_name}')

    @app.route(service_name)
    def on_interest(name, param, _app_param):
        interest = parse_intrest(name)

        # search recently saved data
        res = search_data(q_recent_data, interest['srch'])
        if res is not None:
            # if False:
            # hit
            put_data = res
        else:
            # send interest thread
            # thread_send_interest = threading.Thread(
            #     target=send_interest, args=(q_content, interest['trm'], ))
            # thread_send_interest.start()
            # thread_send_interest.join()
            # data = q_content.get()
            # data = multi_get_content(interest['trm'], 8)
            data = cat_chunks(interest['trm'])

            # call service function
            # svc = time.time()
            put_data = function_relay(data)
            # print(f'service time: {time.time() - svc}')

            # save data
            save_data(q_recent_data, interest['srch'], put_data)
            # print('Saved as {}'.format(interest['srch']))

            # log (get contents)
            with open(logfile, 'a') as f:
                writer = csv.writer(f)
                writer.writerows(q_get.get())

        # put a data packet
        seg_cnt = (len(put_data) + SEGMENT_SIZE - 1) // SEGMENT_SIZE
        if interest['num'] < seg_cnt:
            app.put_data(Name.from_str(interest['srch']) + [Component.from_segment(interest['num'])],
                         put_data[interest['num'] *
                                  SEGMENT_SIZE:(interest['num']+1)*SEGMENT_SIZE],
                         freshness_period=100,
                         final_block_id=Component.from_segment(seg_cnt-1))

            q_put.put([interest['num'], time.time()])

        # log
        if interest['num'] == seg_cnt - 1:
            timestamps = []
            while not q_put.empty():
                n, t = q_put.get()
                timestamps.append(
                    (t, 'relay d-out', Name.to_str(interest['srch']), n))
            with open(logfile, 'a') as f:
                csv.writer(f).writerows(timestamps)

        # print('Restart receiver ...')


if __name__ == '__main__':
    app.run_forever(after_start=main())
