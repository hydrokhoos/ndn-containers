from re import search
from ndn.app import NDNApp
from ndn.encoding import Name
from ndn.encoding import Component
from ndn.encoding.tlv_type import BinaryStr, FormalName
from ndn.types import (InterestCanceled, InterestNack, InterestTimeout,
                       ValidationFailure)
from ndn.app_support.segment_fetcher import segment_fetcher

import threading
import queue
import asyncio as aio
import time


service_name = '/relay'

SEGMENT_SIZE = 4400

q = queue.Queue()
q_recent_data = queue.Queue()

app = NDNApp()


def send_interest(queue, name):
    app_thread = NDNApp()
    async def interest_func(name):
        cnt = 0
        segs = []
        print(f'Sending Interest: {name}')
        async for seg in segment_fetcher(app_thread, name):
            print(f'segment {cnt}: {bytes(seg)[:10]}...')
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
    # just relay
    return data


def save_data(name: str, packets: list):
    while not q_recent_data.empty():
        q_recent_data.get()
    q_recent_data.put({'name': name, 'packets': packets})


def search_data(name: str):
    if q_recent_data.empty():
        return None
    data = q_recent_data.get()
    q_recent_data.put(data)
    if data['name'] == name:
        return data['packets']
    else:
        return None


async def main():
    print('Starting receiver ...')
    @app.route(service_name)
    def on_interest(name, param, _app_param):
        interest_name_org = Name.to_str(name)
        print(f'Received Interest: {interest_name_org}')

        search_name = interest_name_org

        # remove '/relay'(service_name) from interest name
        interest_name_trm = interest_name_org.replace(service_name + '/', '/')

        if Component.get_type(Name.from_str(interest_name_trm)[-1]) == Component.TYPE_SEGMENT:
            num = Component.to_number(Name.from_str(interest_name_trm)[-1])
            interest_name_trm = Name.to_str(interest_name_trm).replace('/seg=' + str(num), '')
            search_name = interest_name_org.replace('/seg=' + str(num), '')

        print(f'Checking recently saved data named {search_name} ...')
        res = search_data(search_name)
        if res is not None:
            print('Data is found.')
            packets = res
            seg_cnt = len(packets)
            if Component.get_type(name[-1]) == Component.TYPE_SEGMENT:
                seg_no = Component.to_number(name[-1])
                print(f'seg_no = {seg_no}')
            else:
                seg_no = 0
            if seg_no < seg_cnt:
                print(f'Putting a packet {seg_no}')
                app.put_raw_packet(packets[seg_no])
                print('Restart receiver ...')
                return
        else:
            print('No data is found. Preparing to send Interest packets ...')

        thread_send_interest = threading.Thread(target=send_interest, args=(q, interest_name_trm, ))
        thread_send_interest.start()
        thread_send_interest.join()

        data = q.get()

        put_data = function_relay(data)

        seg_cnt = (len(put_data) + SEGMENT_SIZE - 1) // SEGMENT_SIZE
        if Component.get_type(Name.from_str(interest_name_org)[-1]) == Component.TYPE_SEGMENT:
            num = Component.to_number(Name.from_str(interest_name_org)[-1])
            interest_name_org = Name.to_str(name).replace('/seg=' + str(num), '')
        print(seg_cnt)
        packets = [app.prepare_data(Name.from_str(interest_name_org) + [Component.from_segment(i)],
                                    put_data[i*SEGMENT_SIZE:(i+1)*SEGMENT_SIZE],
                                    freshness_period=10000,
                                    final_block_id=Component.from_segment(seg_cnt - 1))
                   for i in range(seg_cnt)]

        print(f'Saved as {interest_name_org}.')
        save_data(interest_name_org, packets)

        if Component.get_type(name[-1]) == Component.TYPE_SEGMENT:
            seg_no = Component.to_number(name[-1])
            print(f'seg_no = {seg_no}')
        else:
            seg_no = 0
        if seg_no < seg_cnt:
            print(f'Putting a packet {seg_no}')
            app.put_raw_packet(packets[seg_no])

        print('Restart receiver ...')



if __name__ == '__main__':
    app.run_forever(after_start=main())
