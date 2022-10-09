from ctypes import set_errno
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

# filename = 'test.jpg'
# filename = '/file/abc.txt'
# filename = 'abc.txt'
filename = 'relay/abc.txt'


async def main():
    # Make schema tree
    root = Node()
    # root['/' + filename] = SegmentedNode()
    root[filename] = SegmentedNode()

    # Set policies
    cache = MemoryCache()
    root.set_policy(policy.Cache, MemoryCachePolicy(cache))

    # Attach the tree to the face
    await root.attach(app, '/')

    # Try to fetch target file
    print(f'Try to fetch {filename}...')
    # data, metadata = await root.match('/' + filename).need()
    m = root.match(filename).node
    print(m)
    print(m == root[filename])
    data, metadata = await root.match(filename).need()

    # The file is ready!
    # print(f'Content size: {len(data)}')
    # print(f'Content: {data[:70]} ...')
    # print(f'Number of segments: {metadata["block_count"]}')
    # print(f'Serving {filename}')
    print(metadata)

    # Save file as output file
    output_file = 'fetched-' + filename.replace('/', '-')
    print(f'Data fetched. Saved as {output_file}')
    with open('/node/' + output_file, 'wb') as f:
        f.truncate(0)
        f.write(data)

    app.shutdown()

if __name__ == '__main__':
    app.run_forever(after_start=main())
