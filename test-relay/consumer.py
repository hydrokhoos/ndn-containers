from ndn.app import NDNApp
from ndn.app_support.segment_fetcher import segment_fetcher
from ndn.encoding import Name

import time

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
    async for seg in segment_fetcher(app, target_name, timeout=100000):
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
