from ndn.app import NDNApp
from ndn.app_support.segment_fetcher import segment_fetcher


app = NDNApp()

target_name = '/relay/segments'
# target_name = '/segments'


async def main():
    cnt = 0
    async for seg in segment_fetcher(app, target_name):
        print(bytes(seg))
        cnt += 1
    print(f'{cnt} segments fetched.')
    app.shutdown()


if __name__ == '__main__':
    app.run_forever(after_start=main())
