from dataclasses import dataclass
import sys
import asyncio as aio
import logging
from ndn.app import NDNApp
from ndn.encoding import Name, Component
from ndn.schema import policy
from ndn.schema.schema_tree import MatchedNode, Node
from ndn.schema.simple_node import RDRNode, SegmentedNode
from ndn.schema.simple_cache import MemoryCache, MemoryCachePolicy
from ndn.schema.simple_trust import SignedBy
from ndn.encoding import is_binary_str, FormalName, NonStrictName, Name, Component, \
    SignaturePtrs, InterestParam, BinaryStr, MetaInfo, parse_data, TypeNumber
from typing import Dict, Any, Type, Optional


logging.basicConfig(format='[{asctime}]{levelname}:{message}',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO,
                    style='{')
app = NDNApp()

# filename = 'test.jpg'
filename = 'abc.txt'
filepath = '/node/' + filename

service_name = '/relay'


async def relay_function(data):
    return data


# class RelayNode(SegmentedNode):
#     def __init__(self, parent=None, timeout=4000, retry_times=3, segment_size=...):
#         super().__init__(parent, timeout, retry_times, segment_size)
#         self.parsed_int_name = ''
#         self.data = b''
#         self.processed_data = b''

#     async def process_int(self, match, param, app_param, raw_packet):
#         # print(match.pos == len(match.name))
#         for i in range(1, len(match.name)):
#             print(Component.to_str(match.name[i]))
#             self.parsed_int_name += '/' + Component.to_str(match.name[i])
#         print(f'Parsed interest: {self.parsed_int_name}')
#         print(match.name)
#         print(match.pos, len(match.name))
#         match.name.pop(0)
#         # print(match)
#         print(match.name)
#         print(match.pos, len(match.name))
#         return await super().process_int(match, param, app_param, raw_packet)


class RelayNode(Node):
    async def process_data(self, match, meta_info: MetaInfo, content: Optional[BinaryStr], raw_packet: BinaryStr):
        print('here is process_data')
        print(match.name)
        match.name.insert(0, service_name.replace('/', ''))
        # new_name = service_name
        # for name in match.name:
        #     new_name += '/' + Component.to_str(name)
        match.provide(content, freshness_period=6000)
        return await super().process_data(match, meta_info, content, raw_packet)

    async def process_int(self, match, param: InterestParam, app_param: Optional[BinaryStr], raw_packet: BinaryStr):
        print('here is process_int')
        # print(match)
        match.name.pop(0)
        new_name = ''
        for name in match.name:
            new_name += '/' + Component.to_str(name)
        print(f'new_name: {new_name}')
        submatch = match.finer_match(match.name)
        data, metadata = await submatch.need()


async def main():
    # Make schema tree
    root = Node()
    # root[service_name] = SegmentedNode()
    root[service_name] = RelayNode()
    root['abc.txt'] = SegmentedNode()


    # Set policies
    cache = MemoryCache()
    root.set_policy(policy.Cache, MemoryCachePolicy(cache))

    # Attach the tree to the face
    await root.attach(app, '/')

    # data, metadata = await root.match('abc.txt').need()
    # data_name, metadata, data = await app.express_interest(Name.from_str('/abc.txt'), must_be_fresh=True)
    # print(data)


    # # Read file
    # print(f'Read {filename} from file {filepath}...')
    # with open(filepath, 'rb') as f:
    #     data = f.read()
    #     # Put data
    #     await root.match('/'+filename).provide(data, freshness_period=60000)
    # # await cache.save(Name.normalize('/file/' + filename), data)
    # # await aio.sleep(0.1)

    # # The file is ready! Check content and metadata
    # data, metadata = await root.match('/'+filename).need()
    # print(f'Content size: {len(data)}')
    # print(f'Content: {data[:70]} ...')
    # print(f'Number of segments: {metadata["block_count"]}')
    # print(f'Serving {filename}')

if __name__ == '__main__':
    app.run_forever(after_start=main())
