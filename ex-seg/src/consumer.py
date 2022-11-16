from ndn.app import NDNApp
from ndn.app_support.segment_fetcher import segment_fetcher
from ndn.encoding import Name

import time

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
    async for seg in segment_fetcher(app, target_name, timeout=1000000):
        # print(bytes(seg)[:20])
        # print(cnt)
        data += seg
        cnt += 1
    # print(f'{cnt} segments fetched.')
    # print(f'get time: {time.time() - get}')
    with open(out, 'a') as f:
        f.write(str(len(data)/1024)+','+str(time.time()-get)+'\n')

    with open(filepath + fetchedfile, 'wb') as f:
        f.write(data)
    app.shutdown()


if __name__ == '__main__':
    app.run_forever(after_start=main())
