from ndn.app import NDNApp
from ndn.encoding import Name, Component

import time
import queue
import csv


SEGMENT_SIZE = 4400

filepath = '/src/'

# with open(filepath + 'target_name', 'r') as f:
#     target_name = f.read().strip()
target_name = 'img2.jpg'
logfile = filepath + 'producer2.csv'
with open(filepath + target_name, 'rb') as f:
    data = f.read()
target_name = Name.normalize(target_name)


def main():
    app = NDNApp()

    seg_cnt = (len(data) + SEGMENT_SIZE - 1) // SEGMENT_SIZE
    packets = [app.prepare_data(target_name + [Component.from_segment(i)],
                                    data[i*SEGMENT_SIZE:(i+1)*SEGMENT_SIZE],
                                    freshness_period=1000,
                                    final_block_id=Component.from_segment(seg_cnt - 1))
                   for i in range(seg_cnt)]
    print(f'Created {seg_cnt} chunks under name {Name.to_str(target_name)}')

    time_q = queue.Queue(maxsize=seg_cnt)

    @app.route(target_name)
    def on_interest(int_name, _int_param, _app_param):
        # print(f'Recieved Interest:\t{Name.to_str(int_name)}')
        if Component.get_type(int_name[-1]) == Component.TYPE_SEGMENT:
            seg_no = Component.to_number(int_name[-1])
        else:
            seg_no = 0
        if seg_no < seg_cnt:
            # print(f'Putting a packet:\t{seg_no}')
            app.put_raw_packet(packets[seg_no])

            ### log
            time_q.put([seg_no, time.time()])
            if time_q.full():
                timestamps = []
                # complete all segments
                n0, t0 = time_q.get()
                # timestamps.append([n0, 0])
                timestamps.append((t0, 'producer2 d-out', Name.to_str(target_name), n0))
                while not time_q.empty():
                    n, t = time_q.get()
                    # timestamps.append([n, t-t0])
                    timestamps.append((t, 'producer2 d-out', Name.to_str(target_name), n))
                # puttime = timestamps[-1][1] - timestamps[0][1]
                # puttime = timestamps[-1][0] - timestamps[0][0]
                with open(logfile, 'a') as f:
                    writer = csv.writer(f)
                    # writer.writerow(('time', 'action', 'name', 'segment number'))
                    writer.writerows(timestamps)
                # with open(filepath + csvfile, 'a') as f:
                #     writer = csv.writer(f)
                #     writer.writerow([len(data)/1024, puttime])


    app.run_forever()


if __name__ == '__main__':
    main()
