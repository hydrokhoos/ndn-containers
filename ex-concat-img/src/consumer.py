from ndn.app import NDNApp
from ndn.app_support.segment_fetcher import segment_fetcher
from ndn.encoding import Name

import time
import csv

app = NDNApp()

relay = False

filepath = '/src/'
ext = '.jpg'

target_name = '/concatimg/img1'+ext+'-img2'+ext
# target_name = '/img2' + ext
# with open(filepath + 'target_name', 'r') as f:
#     target_name = f.read().strip()
logfile = filepath + 'consumer.csv'
if relay:
    target_name = '/relay/' + target_name
target_name = Name.normalize(target_name)
fetchedfile = 'fetched' + Name.to_str(target_name).replace('/', '-')
fetchedfile = fetchedfile.replace('.', '').replace(',', '') + ext

async def main():
    get = time.time()
    cnt = 0
    data = b''
    timestamps = []
    async for seg in segment_fetcher(app, target_name, timeout=100000000):
        data += seg
        cnt += 1
        timestamps.append((str(time.time()), 'consumer d-in', Name.to_str(target_name), str(cnt)))
    with open(filepath + fetchedfile, 'wb') as f:
        f.write(data)
    get = time.time() - get

    ### log
    with open('/src/cgettime', 'a') as f:
        # csv.writer(f).writerow(str(len(data/1024)) + ',' + str(get))
        f.write(str(len(data)/1024)+','+str(get)+'\n')

    with open(logfile, 'a') as f:
        writer = csv.writer(f)
        # writer.writerow(('time', 'action', 'name', 'segment number'))
        writer.writerows(timestamps)

    app.shutdown()


if __name__ == '__main__':
    app.run_forever(after_start=main())
