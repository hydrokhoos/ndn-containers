from ndn.app import NDNApp
from ndn.encoding import Name
from ndn.types import (InterestCanceled, InterestNack, InterestTimeout,
                       ValidationFailure)


app = NDNApp()

service_name = '/relay'

relay_info = {'original_interest_name': '', 'trim_interest_name': '', 'original_data': b'', 'relaid_data': b''}


def receive_interest():
    @app.route(service_name)
    def on_interest(name, param, _app_param):
        print(f'Received Interest:\t{Name.to_str(name)}')

        # remove '/relay'(service_name) from interest name
        relay_info['original_interest_name'] = Name.to_str(name)
        relay_info['trim_interest_name'] = (Name.to_str(name)).replace(service_name + '/', '/')

        app.shutdown()


    print('Start receiver ...')
    app.run_forever()


def send_interest():
    async def main():
        try:
            print(f'Sending Interest:\t{Name.to_str(name)}')
            data_name, meta_info, content = await app.express_interest(name, must_be_fresh=True, can_be_prefix=False, lifetime=6000)
            print(f'Received Data Name:\t{Name.to_str(data_name)}')
            relay_info['original_data'] = bytes(content) if content else None
        except InterestNack as e:
            print(f'Nacked with reason={e.reason}')
        except InterestTimeout:
            print(f'Timeout')
        except InterestCanceled:
            print(f'Canceled')
        except ValidationFailure:
            print(f'Data failed to validate')
        finally:
            app.shutdown()


    name = Name.from_str(relay_info['trim_interest_name'])

    app.run_forever(after_start=main())


def send_data():
    async def main():
        print(f'Putting Data Name:\t{relay_info["original_interest_name"]}')
        app.put_data(Name.from_str(relay_info['original_interest_name']), content=relay_info['relaid_data'], freshness_period=100000)
        app.shutdown()


    app.run_forever(after_start=main())


if __name__ == '__main__':
    receive_interest()

    send_interest()

    # just relay
    relay_info['relaid_data'] = relay_info['original_data']

    send_data()

    # print()
    # print(relay_info)
