from ndn.app import NDNApp
from ndn.app_support.segment_fetcher import segment_fetcher
from ndn.encoding import Name, Component, NonStrictName, FormalName
from ndn.types import InterestTimeout

import time
import threading
import queue


from concurrent import futures
def multi_get_content(name: NonStrictName, final: int) -> bytes:
    def _get_a_segment(_name: NonStrictName, _seg_no: int, _q: queue.Queue):
        async def ex_int(_name: NonStrictName, _q: queue):
            _n, _m, _c = await _app.express_interest(_name, must_be_fresh=True)
            _q.put([_seg_no, _c])
            _app.shutdown()
        _app = NDNApp()
        _app.run_forever(after_start=ex_int(_name+[Component.from_segment(_seg_no)], _q))

    data_q = queue.Queue()
    future_list = []
    with futures.ThreadPoolExecutor(max_workers=4) as executor:
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


def get_final(name: NonStrictName):
    def _get_a_seg(_name, _q):
        async def _ex_int(_name, _q):
            print(f'putting inteterest {Name.to_str(_name)}')
            _n, _m, _c = await _app.express_interest(_name+[Component.from_segment(0)], must_be_fresh=True)
            print('put interest')
            if Component.get_type(_n[-1]) == Component.TYPE_SEGMENT:
                _q.put(Component.to_number(_m.final_block_id))
            else:
                _q.put(0)
            _app.shutdown()
        _app = NDNApp()
        _app.run_forever(after_start=_ex_int(_name, _q))

    q = queue.Queue()
    thread = threading.Thread(target=_get_a_seg, args=(name, q, ))
    print(f'THREAD START {Name.to_str(name)}')
    thread.start()
    thread.join()
    return q.get()



app = NDNApp()

relay = False

filepath = '/src/'
out = filepath + 'result.csv'
with open(filepath + 'target_name', 'r') as f:
    target_name = f.read().strip()

if relay:
    target_name = '/relay/' + target_name

target_name = Name.normalize(target_name)
fetchedfile = 'fetched' + Name.to_str(target_name).replace('/', '-')

async def main():
    cnt = 0
    data = b''
    get = time.time()

    final = get_final(target_name)

    print(f'final block id: {final}')
    if final == 0:
        async for seg in segment_fetcher(app, target_name):
            data += seg
            cnt += 1
    else:
        data = multi_get_content(target_name, final)
    # print(f'get time: {round(time.time() - get, 5)}')
    with open(out, 'a') as f:
        f.write(str(len(data)/1024)+','+str(time.time()-get)+'\n')

    with open(filepath + fetchedfile, 'wb') as f:
        f.truncate(0)
        f.write(data)
    app.shutdown()


if __name__ == '__main__':
    app.run_forever(after_start=main())
