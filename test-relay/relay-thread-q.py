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
# import cv2


service_name = '/relay'

SEGMENT_SIZE = 4400
FRESHNESS_PERIOD = 100000

q_content = queue.Queue()
q_recent_data = queue.Queue()

app = NDNApp()


def send_interest(queue: queue.Queue, name: FormalName) -> None:
    async def interest_func(name):
        cnt = 0
        data = b''
        # print(f'Sending Interest: {name}')
        async for seg in segment_fetcher(app_thread, name, timeout=4000, retry_times=3):
            # print(f'segment {cnt}: {bytes(seg)[:10]}...')
            data += seg
            with open('/test-relay/log-r.csv', 'a') as f:
                f.write(str(cnt) + ', ' + str(time.time()) + ', GET\n')
            cnt += 1
        # print(f'{cnt} segments fetched.')
        queue.put(data)
        app_thread.shutdown()

    if not queue.empty():
        app_thread.shutdown()
        return
    app_thread = NDNApp()
    app_thread.run_forever(after_start=interest_func(name))


def function_relay(data: bytes) -> bytes:
    # just relay
    return data


def function_delay(data: bytes) -> bytes:
    # wait 5sec
    time.sleep(5)
    return data

# def function_gray(data: bytes) -> bytes:
#     file = '/img.jpg'
#     with open(file, 'wb') as f:
#         f.truncate(0)
#         f.write(data)

#     img = cv2.imread(file)
#     with open(file, 'wb') as f:
#         f.truncate(0)

#     img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#     threshold = 100
#     ret, th_img = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)

#     cv2.imwrite(file, th_img)

#     out = b''
#     with open(file, 'rb') as f:
#         out = f.read()
#     return out


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

        # print('Received Interest: {}'.format(interest['org']))

        # search recently saved data
        # print('Checking recently saved data named {} ...'.format(interest['org']))
        res = search_data(q_recent_data, interest['srch'])
        if res is not None:
            # hit
            # print('Data is found.')
            put_data = res
        else:
            # print('No data is found.')
            # print('Getting original contents ...')

            # send interest thread
            thread_send_interest = threading.Thread(target=send_interest, args=(q_content, interest['trm'], ))
            thread_send_interest.start()
            thread_send_interest.join()
            data = q_content.get()

            # call service function
            # print('Calling function ...')
            put_data = function_relay(data)
            # put_data = function_delay(data)
            # put_data = function_gray(data)

            # save data
            save_data(q_recent_data, interest['srch'], put_data)
            # print('Saved as {}'.format(interest['srch']))

        # put a data packet
        seg_cnt = (len(put_data) + SEGMENT_SIZE - 1) // SEGMENT_SIZE
        if interest['num'] < seg_cnt:
            # print('Putting a packet {}/{}'.format(interest['num']+1, seg_cnt))
            app.put_data(Name.from_str(interest['srch']) + [Component.from_segment(interest['num'])],
                         put_data[interest['num']*SEGMENT_SIZE:(interest['num']+1)*SEGMENT_SIZE],
                         freshness_period=100,
                         final_block_id=Component.from_segment(seg_cnt-1))
            with open('/test-relay/log-r.csv', 'a') as f:
                f.write(str(interest['num']) + ', ' + str(time.time()) + ', PUT\n')

        # print('Restart receiver ...')



if __name__ == '__main__':
    app.run_forever(after_start=main())
