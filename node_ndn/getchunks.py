from ndn.app import NDNApp
from ndn.app_support.segment_fetcher import segment_fetcher


app = NDNApp()

# target_name = '/relay/segments'
# target_name = '/segments'
# target_name = '/file/test.jpg'
# target_name = '/test.jpg'
# target_name = '/relay/file/abc.txt'
target_name = '/file/abc.txt'


async def main():
    cnt = 0
    async for seg in segment_fetcher(app, target_name):
        print(bytes(seg)[:20])
        cnt += 1
    print(f'{cnt} segments fetched.')
    app.shutdown()


if __name__ == '__main__':
    app.run_forever(after_start=main())
