from fileinput import filename
from ndn.utils import timestamp
from ndn.app import NDNApp
from ndn.encoding import Name, Component


SEGMENT_SIZE = 10

filename = 'abc.txt'
filepath = '/node/abc.txt'
filename = Name.normalize(filename)


def main():
    app = NDNApp()

    name = filename
    # name.append(Component.from_version(timestamp()))

    # data = b'abcdefghijklmnopqrstuvwxyz'
    with open(filepath, 'rb') as f:
        data = f.read()
    seg_cnt = (len(data) + SEGMENT_SIZE - 1) // SEGMENT_SIZE
    packets = [app.prepare_data(name + [Component.from_segment(i)],
                                    data[i*SEGMENT_SIZE:(i+1)*SEGMENT_SIZE],
                                    freshness_period=10000,
                                    final_block_id=Component.from_segment(seg_cnt - 1))
                   for i in range(seg_cnt)]
    print(f'Created {seg_cnt} chunks under name {Name.to_str(name)}')


    @app.route(name)
    def on_interest(int_name, _int_param, _app_param):
        print(f'Recieved Interest:\t{Name.to_str(name)}')
        if Component.get_type(int_name[-1]) == Component.TYPE_SEGMENT:
            seg_no = Component.to_number(int_name[-1])
        else:
            seg_no = 0
        if seg_no < seg_cnt:
            print(f'Putting a packet:\t{seg_no}')
            app.put_raw_packet(packets[seg_no])

    app.run_forever()


if __name__ == '__main__':
    main()
