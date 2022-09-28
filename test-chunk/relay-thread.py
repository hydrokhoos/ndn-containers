from ndn.app import NDNApp
from ndn.encoding import Name
from ndn.encoding import Component
from ndn.types import (InterestCanceled, InterestNack, InterestTimeout,
                       ValidationFailure)
from ndn.app_support.segment_fetcher import segment_fetcher

import threading
import queue


service_name = '/relay'

SEGMENT_SIZE = 10

q = queue.Queue()


def send_interest(queue, name):
    app_thread = NDNApp()
    async def interest_func(name):
        cnt = 0
        segs = []
        print(f'Sending Interest:\t{name}')
        async for seg in segment_fetcher(app_thread, name):
            print(f'segment {cnt}:\t{bytes(seg)}')
            segs.append(seg)
            cnt += 1
        print(f'{cnt} segments fetched.')
        data = b''
        for seg in segs:
            data += bytes(seg)
        queue.put(data)

        app_thread.shutdown()

    if not q.empty():
        app_thread.shutdown()
        return
    app_thread.run_forever(after_start=interest_func(name))


def function_relay(data):
    # additional contents
    data += b'123456789'
    return data


def main():
    app = NDNApp()

    @app.route(service_name)
    def on_interest(name, param, _app_param):
        print(f'Received Interest:\t{Name.to_str(name)}')

        # remove '/relay'(service_name) from interest name
        interest_name_org = Name.to_str(name)
        interest_name_trm = (Name.to_str(name)).replace(service_name + '/', '/')

        if Component.get_type(Name.from_str(interest_name_trm)[-1]) == Component.TYPE_SEGMENT:
            num = Component.to_number(Name.from_str(interest_name_trm)[-1])
            interest_name_trm = Name.to_str(interest_name_trm).replace('/seg=' + str(num), '')

        thread_send_interest = threading.Thread(target=send_interest, args=(q, interest_name_trm, ))
        thread_send_interest.start()
        thread_send_interest.join()

        data = q.get()

        put_data = function_relay(data)

        seg_cnt = (len(put_data) + SEGMENT_SIZE - 1) // SEGMENT_SIZE
        if Component.get_type(Name.from_str(interest_name_org)[-1]) == Component.TYPE_SEGMENT:
            num = Component.to_number(Name.from_str(interest_name_org)[-1])
            interest_name_org = Name.to_str(name).replace('/seg=' + str(num), '')
        packets = [app.prepare_data(Name.from_str(interest_name_org) + [Component.from_segment(i)],
                                    put_data[i*SEGMENT_SIZE:(i+1)*SEGMENT_SIZE],
                                    freshness_period=10000,
                                    final_block_id=Component.from_segment(seg_cnt - 1))
                   for i in range(seg_cnt)]

        if Component.get_type(name[-1]) == Component.TYPE_SEGMENT:
            seg_no = Component.to_number(name[-1])
            print(f'seg_no = {seg_no}')
        else:
            seg_no = 0
        if seg_no < seg_cnt:
            print(f'Putting a packet {seg_no}')
            app.put_raw_packet(packets[seg_no])

        print('Restert receiver ...')


    print('Start receiver ...')
    app.run_forever()


if __name__ == '__main__':
    main()
