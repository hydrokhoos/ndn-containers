from ndn.app import NDNApp
from ndn.app_support.segment_fetcher import segment_fetcher
from ndn.encoding import Name, Component, NonStrictName
from ndn.types import InterestTimeout

import time
import threading
import queue

async def kami_segment_fetcher(app: NDNApp, name: NonStrictName,
                               final: int, timeout=4000, retry_times=3,
                               validator=None, must_be_fresh=True):

    async def retry(first):
        nonlocal name
        trial_times = 0
        while True:
            future = app.express_interest(name, validator=validator, can_be_prefix=first,
                                          must_be_fresh=must_be_fresh, lifetime=timeout)
            try:
                return await future
            except InterestTimeout:
                trial_times += 1
                if trial_times >= retry_times:
                    raise

    name = Name.normalize(name)
    seg_no = 0
    # timestamps = []
    while True:
        if seg_no == 0:
            name, meta, content = await retry(True)
            # timestamps.append(time.time())
        else:
            name[-1] = Component.from_segment(seg_no)
            name, meta, content = await retry(False)
            # timestamps.append(time.time())
        yield content
        if Component.to_number(name[-1]) == final:
            # m = min(timestamps)
            # for i, ts in enumerate(timestamps):
            #     print(f'ts {i}: {round(ts-m, 3)}')
            return
        seg_no += 1

async def simple_get_content(app:NDNApp, name: NonStrictName, start:int, final: int) -> bytes:
    data = b''
    timestamps = []
    for i in range(start, final+1):
        _name, _meta, _content = await app.express_interest(name + [Component.from_segment(i)], must_be_fresh=True)
        timestamps.append(time.time())
        data += _content
    for i, ts in enumerate(timestamps):
        print(f'ts {i}: {round(ts-min(timestamps), 3)}')
    return data


def part_get_content(name: NonStrictName, start: int, stop: int, out: queue) -> bytes:
    async def ex_int(_name, _start, _stop, _q):
        data = b''
        for i in range(_start, _stop):
            _n, _m, _c = await _app.express_interest(_name + [Component.from_segment(i)], must_be_fresh=True)
            data += _c
        _q.put(data)
        _app.shutdown()

    _app = NDNApp()
    _app.run_forever(after_start=ex_int(name, start, stop, out))


from concurrent import futures
def mult_get_content(name: NonStrictName, final: int) -> bytes:
    def _get_a_segment(_name: NonStrictName, _seg_no: int, _q: queue):
        async def ex_int(_name, _q):
            _n, _m, _c = await _app.express_interest(_name, must_be_fresh=True)
            _q.put([_seg_no, _c])
            _app.shutdown()
        _app = NDNApp()
        _app.run_forever(after_start=ex_int(_name+[Component.from_segment(_seg_no)], _q))

    data_q = queue.Queue()
    future_list = []
    with futures.ThreadPoolExecutor(max_workers=3) as executor:
        for i in range(final+1):
            future = executor.submit(_get_a_segment, _name=name, _seg_no=i, _q=data_q)
            future_list.append(future)
        _ = futures.as_completed(fs=future_list)

    data_list = []
    while not data_q.empty():
        data_list.append(data_q.get())
    print(f'{len(data_list)} segments fetched.')
    data_list = sorted(data_list, reverse=False, key=lambda x: x[0])
    ret = b''
    for data in data_list:
        ret += data[1]
    return ret


app = NDNApp()

relay = True

filepath = '/test-relay/'
with open(filepath + 'target_name.txt', 'r') as f:
    target_name = f.read().strip()

if relay:
    target_name = '/relay/' + target_name

target_name = Name.normalize(target_name)
outputfile = 'fetched' + Name.to_str(target_name).replace('/', '-')

async def main():
    cnt = 0
    data = b''
    get = time.time()
    # async for seg in kami_segment_fetcher(app, target_name, 8, timeout=4000):
    # async for seg in segment_fetcher(app, target_name, timeout=4000):
        # print(bytes(seg)[:20])
        # print(cnt)
        # data += seg
        # cnt += 1
    # print(f'{cnt} segments fetched.')

    # data1 = await simple_get_content(app, target_name, 0, 3)
    # data2 = await simple_get_content(app, target_name, 4, 8)
    # data = data1 + data2

    # q1 = queue.Queue()
    # q2 = queue.Queue()
    # thread1 = threading.Thread(target=part_get_content, args=(target_name, 0, 4, q1, ))
    # thread2 = threading.Thread(target=part_get_content, args=(target_name, 4, 9, q2, ))
    # thread1.start()
    # thread2.start()
    # thread1.join()
    # thread2.join()
    # data = q1.get() + q2.get()

    data = mult_get_content(target_name, 8)

    print(f'get time: {time.time() - get}')

    # with open('/test-relay/log.txt', 'a') as f:
    #     f.write(str(time.time()) + '\n')

    with open(filepath + outputfile, 'wb') as f:
        f.truncate(0)
        f.write(data)
    app.shutdown()


if __name__ == '__main__':
    app.run_forever(after_start=main())
