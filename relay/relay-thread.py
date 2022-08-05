from ndn.app import NDNApp
from ndn.encoding import Name
from ndn.types import (InterestCanceled, InterestNack, InterestTimeout,
                       ValidationFailure)

import threading
import queue


service_name = '/relay'

q = queue.Queue()


def send_interest(queue, name):
    app_thread = NDNApp()
    async def interest_func(name):
        print(f'Sending Interest:\t{name}')
        data_name, meta_info, content = await app_thread.express_interest(name, must_be_fresh=True, can_be_prefix=False, lifetime=6000)
        print('Data received')
        queue.put((data_name, meta_info, bytes(content)))
        app_thread.shutdown()

    app_thread.run_forever(after_start=interest_func(name))


def function_relay(data):
    # just relay
    return data


def main():
    app = NDNApp()
    @app.route(service_name)
    def on_interest(name, param, _app_param):
        print(f'Received Interest:\t{Name.to_str(name)}')

        # remove '/relay'(service_name) from interest name
        interest_name_org = Name.to_str(name)
        interest_name_trm = (Name.to_str(name)).replace(service_name + '/', '/')

        thread_send_interest = threading.Thread(target=send_interest, args=(q, interest_name_trm, ))
        thread_send_interest.start()
        thread_send_interest.join()

        data_name, meta_info, content = q.get()

        put_data = function_relay(content)

        print(f'Putting Data Name:\t{interest_name_org}')
        app.put_data(Name.from_str(interest_name_org), content=put_data, freshness_period=100000)


    print('Start receiver ...')
    app.run_forever()


if __name__ == '__main__':
    main()
