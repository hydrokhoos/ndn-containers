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
    async for seg in segment_fetcher(app, target_name, timeout=100000):
        # print(bytes(seg)[:20])
        # print(cnt)
        data += seg
        with open('/test-relay/log-c.csv', 'a') as f:
            f.write(str(cnt) + ', ' + str(time.time()) + '\n')
        cnt += 1
    print(f'{cnt} segments fetched.')

    # with open('/test-relay/log.txt', 'a') as f:
    #     f.write(str(time.time()) + '\n')

    with open(filepath + outputfile, 'wb') as f:
        f.truncate(0)
        f.write(data)
    app.shutdown()


if __name__ == '__main__':
    t = time.time()
    app.run_forever(after_start=main())
    print(str(time.time()-t)[:6] + 's')
