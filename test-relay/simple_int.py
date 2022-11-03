import logging, sys
import ndn.utils
from ndn.app import NDNApp
from ndn.types import InterestNack, InterestTimeout, InterestCanceled, ValidationFailure
from ndn.encoding import Name, Component, InterestParam


app = NDNApp()

name = '/segments/seg=1'


async def main():
    print(f'Sending Interest {Name.to_str(name)}')
    data_name, meta_info, content = await app.express_interest(name, must_be_fresh=True, can_be_prefix=False, lifetime=6000)

    print(f'Received Data Name: {Name.to_str(data_name)}')
    # print(meta_info)
    print(bytes(content) if content else None)
    app.shutdown()


if __name__ == '__main__':
    app.run_forever(after_start=main())
