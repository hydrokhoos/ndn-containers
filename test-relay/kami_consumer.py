from ndn.app import NDNApp
from ndn.app_support.segment_fetcher import segment_fetcher
from ndn.encoding import Name, Component, NonStrictName
from ndn.types import InterestTimeout

import time


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
    while True:
        if seg_no == 0:
            name, meta, content = await retry(True)
        else:
            name[-1] = Component.from_segment(seg_no)
            name, meta, content = await retry(False)
        yield content
        if Component.to_number(name[-1]) == final:
            return
        seg_no += 1


app = NDNApp()

relay = False

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
    async for seg in kami_segment_fetcher(app, target_name, 8, timeout=100000):
    # async for seg in segment_fetcher(app, target_name, timeout=100000):
        # print(bytes(seg)[:20])
        # print(cnt)
        data += seg
        cnt += 1
    print(f'{cnt} segments fetched.')
    print(f'get time: {time.time() - get}')

    # with open('/test-relay/log.txt', 'a') as f:
    #     f.write(str(time.time()) + '\n')

    with open(filepath + outputfile, 'wb') as f:
        f.truncate(0)
        f.write(data)
    app.shutdown()


if __name__ == '__main__':
    app.run_forever(after_start=main())
