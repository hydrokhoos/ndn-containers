from ndn.app import NDNApp
from ndn.encoding import Component, Name
import time


app = NDNApp()

SEGMENT_SIZE = 1000

name = 'theta.jpg'
interest_name_org = '/relay/theta.jpg/seg=2'

Name.normalize(name)
Name.normalize(interest_name_org)

t = time.time()
with open('theta.jpg', 'rb') as f:
    data = f.read()
print(f'read: {time.time() - t}')

seg_cnt = (len(data) + SEGMENT_SIZE - 1) // SEGMENT_SIZE
if Component.get_type(Name.from_str(interest_name_org)[-1]) == Component.TYPE_SEGMENT:
    num = Component.to_number(Name.from_str(interest_name_org)[-1])
    interest_name_org = Name.to_str(name).replace('/seg=' + str(num), '')
# print(seg_cnt)
t = time.time()
packets = [app.prepare_data(Name.from_str(interest_name_org) + [Component.from_segment(i)],
                            data[i*SEGMENT_SIZE:(i+1)*SEGMENT_SIZE],
                            freshness_period=10000,
                            final_block_id=Component.from_segment(seg_cnt - 1))
            for i in range(seg_cnt)]
print(f'full seg: {time.time() - t}')
t = time.time()
packet = app.prepare_data(Name.from_str(interest_name_org) + [Component.from_segment(num)],
                          data[num*SEGMENT_SIZE:(num+1)*SEGMENT_SIZE],
                          freshness_period=10000,
                          final_block_id=Component.from_segment(seg_cnt - 1))
print(f'1 seg: {time.time() - t}')
