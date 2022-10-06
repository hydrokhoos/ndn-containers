import sys
import asyncio as aio
import logging
from ndn.app import NDNApp
from ndn.encoding import Name
from ndn.schema import policy
from ndn.schema.schema_tree import Node
from ndn.schema.simple_node import RDRNode, SegmentedNode
from ndn.schema.simple_cache import MemoryCache, MemoryCachePolicy
from ndn.schema.simple_trust import SignedBy


logging.basicConfig(format='[{asctime}]{levelname}:{message}',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO,
                    style='{')
app = NDNApp()

filename = 'test.jpg'
filepath = '/node/' + filename


async def main():
    # Make schema tree
    root = Node()
    # root['/file/<FileName>'] = RDRNode()
    root['/file/' + filename] = RDRNode()
    # root['/file/' + filename] = SegmentedNode()

    # Set policies
    cache = MemoryCache()
    root.set_policy(policy.Cache, MemoryCachePolicy(cache))

    # Attach the tree to the face
    await root.attach(app, '/')

    # Read file
    print(f'Read {filename} from file {filepath}...')
    with open(filepath, 'rb') as f:
        data = f.read()
        # Put data
        await root.match('/file/' + filename).provide(data, freshness_period=60000)
    # await cache.save(Name.normalize('/file/' + filename), data)
    # await aio.sleep(0.1)

    # The file is ready! Check content and metadata
    data, metadata = await root.match('/file/' + filename).need()
    print(f'Content size: {len(data)}')
    print(f'Content: {data[:70]} ...')
    print(f'Number of segments: {metadata["block_count"]}')
    print(f'Serving {filename}')

if __name__ == '__main__':
    app.run_forever(after_start=main())
