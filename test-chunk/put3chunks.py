from ndn.utils import timestamp
from ndn.app import NDNApp
from ndn.encoding import Name, Component


def main():
    app = NDNApp()

    name = Name.normalize('segments')
    # name.append(Component.from_version(timestamp()))

    seg_cnt = 3
    segs = ['first segment', 'second segment', 'third segment']
    packets = [app.prepare_data(name + [Component.from_segment(i)],
                                    segs[i].encode(),
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
