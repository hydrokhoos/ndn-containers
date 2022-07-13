from operator import truediv
from ndn.app import NDNApp
from ndn.encoding import Name
from ndn.types import InterestCanceled, InterestNack, InterestTimeout, ValidationFailure


# app = NDNApp()

service_name = '/relay'


class Relayinfo:
    def __init__(self):
        self.int_name_org = ''
        self.int_name_trm = ''
        self.dat_org = b''
        self.dat_rld = b''
        self.is_interest_received = False

    def trim_int_name(self):
        self.int_name_trm = self.int_name_org.replace(service_name + '/', '/')

    def relay_data(self):
        self.dat_rld = self.dat_org

    def print_info(self):
        print('#####')
        print(self.int_name_org)
        print(self.int_name_trm)
        print(self.dat_org)
        print(self.dat_rld)
        print('#####')

    def receive_interest(self):
        @app.route(service_name)
        def on_interest(name, param, _app_param):
            self.int_name_org = Name.to_str(name)
            print(f'Received Interest:\t{self.int_name_org}')
            self.is_interest_received = True

            # remove '/relay'(service_name) from interest name
            self.trim_int_name()

            app.shutdown()

        print('Start receiver ...')
        app.run_forever()

    def send_interest(self):
        async def main():
            try:
                print(f'Sending Interest:\t{Name.to_str(name)}')
                data_name, meta_info, content = await app.express_interest(name, must_be_fresh=True, can_be_prefix=False, lifetime=6000)
                print(f'Received Data Name:\t{Name.to_str(data_name)}')
                self.dat_org = bytes(content)
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

        name = Name.from_str(self.int_name_trm)

        app.run_forever(after_start=main())

    def send_data(self):
        async def main():
            print(f'Putting Data Name:\t{self.int_name_org}')
            app.put_data(Name.from_str(self.int_name_org), content=self.dat_rld, freshness_period=100000)
            app.shutdown()

        app.run_forever(after_start=main())


if __name__ == '__main__':
    while True:
        app = NDNApp()

        relay = Relayinfo()

        relay.receive_interest()

        if relay.is_interest_received:
            relay.send_interest()
        else:
            print('Stop receiver ...')
            break

        # just relay
        relay.relay_data()

        relay.send_data()

        relay.print_info()
