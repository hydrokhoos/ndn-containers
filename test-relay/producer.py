from ndn.utils import timestamp
from ndn.app import NDNApp
from ndn.encoding import Name, Component

import time


SEGMENT_SIZE = 4400

filepath = '/test-relay/'
with open(filepath + 'target_name.txt', 'r') as f:
    name = f.read().strip()
with open(filepath + name, 'rb') as f:
    data = f.read()
name = Name.normalize(name)

def main():
    app = NDNApp()

    # name = Name.normalize('segments')
    # name.append(Component.from_version(timestamp()))

    # data = b'abcdefghijklmnopqrstuvwxyz'
    seg_cnt = (len(data) + SEGMENT_SIZE - 1) // SEGMENT_SIZE
    packets = [app.prepare_data(name + [Component.from_segment(i)],
                                    data[i*SEGMENT_SIZE:(i+1)*SEGMENT_SIZE],
                                    freshness_period=10000,
                                    final_block_id=Component.from_segment(seg_cnt - 1))
                   for i in range(seg_cnt)]
    print(f'Created {seg_cnt} chunks under name {Name.to_str(name)}')


    @app.route(name)
    def on_interest(int_name, _int_param, _app_param):
        # print(f'Recieved Interest:\t{Name.to_str(int_name)}')
        if Component.get_type(int_name[-1]) == Component.TYPE_SEGMENT:
            seg_no = Component.to_number(int_name[-1])
        else:
            seg_no = 0
        if seg_no < seg_cnt:
            # with open('/test-relay/log.txt', 'a') as f:
            #     f.write('Producer' + ' ' + Name.to_str(int_name) + ' ' + str(time.time()) + '\n')
            # print(f'Putting a packet:\t{seg_no}')
            with open('/test-relay/log-p.csv', 'a') as f:
                f.write(str(seg_no) + ', ' + str(time.time()) + '\n')
            app.put_raw_packet(packets[seg_no])
            # if seg_no + 1 == seg_cnt:
            #     with open('/test-relay/log.txt', 'a') as f:
            #         f.truncate(0)
            #         f.write(str(time.time()) + '\n')

    app.run_forever()


if __name__ == '__main__':
    main()
