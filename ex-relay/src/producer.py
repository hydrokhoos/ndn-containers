from ndn.app import NDNApp
from ndn.encoding import Name, Component

import time
import queue
import csv


SEGMENT_SIZE = 4400

filepath = '/src/'
csvfile = 'producer.csv'

with open(filepath + 'target_name', 'r') as f:
    name = f.read().strip()
with open(filepath + name, 'rb') as f:
    data = f.read()
name = Name.normalize(name)


def main():
    app = NDNApp()

    seg_cnt = (len(data) + SEGMENT_SIZE - 1) // SEGMENT_SIZE
    packets = [app.prepare_data(name + [Component.from_segment(i)],
                                    data[i*SEGMENT_SIZE:(i+1)*SEGMENT_SIZE],
                                    freshness_period=1000,
                                    final_block_id=Component.from_segment(seg_cnt - 1))
                   for i in range(seg_cnt)]
    print(f'Created {seg_cnt} chunks under name {Name.to_str(name)}')

    time_q = queue.Queue(maxsize=seg_cnt)

    @app.route(name)
    def on_interest(int_name, _int_param, _app_param):
        # print(f'Recieved Interest:\t{Name.to_str(int_name)}')
        if Component.get_type(int_name[-1]) == Component.TYPE_SEGMENT:
            seg_no = Component.to_number(int_name[-1])
        else:
            seg_no = 0
        if seg_no < seg_cnt:
            # print(f'Putting a packet:\t{seg_no}')
            app.put_raw_packet(packets[seg_no])

            # timestamps
            # time_q.put([seg_no, time.time()])
            # if time_q.full():
            #     l = []
            #     # complete all segments
            #     n0, t0 = time_q.get()
            #     print(f'{n0}, 0')
            #     l.append([n0, 0])
            #     while not time_q.empty():
            #         n, t = time_q.get()
            #         print(f'{n}, {round(t - t0, 5)}')
            #         l.append([n, t-t0])
            #     print(f'put time: {round(t - t0, 5)}\n')
            #     with open(filepath + csvfile, 'w') as f:
            #         writer = csv.writer(f)
            #         writer.writerows(l)


    app.run_forever()


if __name__ == '__main__':
    main()
