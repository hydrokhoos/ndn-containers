from ndn.app import NDNApp
from ndn.encoding import Name
from ndn.types import InterestNack, InterestTimeout, InterestCanceled, ValidationFailure


app = NDNApp()

service_name = '/relay'
l = []

def receive_interest():
    @app.route(service_name)
    def on_interest(name, param, _app_param):
        # remove '/relay'(service_name) from interest name
        print(f'Received Interest: {Name.to_str(name)}')
        tmp_name = (Name.to_str(name)).replace(service_name + '/', '/')
        name = Name.from_str(tmp_name)
        l.append(tmp_name)

        app.shutdown()

    print('Start receiver ...')
    app.run_forever()


def send_interest():
    async def main():
        try:
            print(f'Sending Interest: {Name.to_str(name)}')
            data_name, meta_info, content = await app.express_interest(name, must_be_fresh=True, can_be_prefix=False, lifetime=6000)
            print(f'Received Data: {Name.to_str(data_name)}')
            # print(meta_info)
            # print(bytes(content) if content else None)
        except InterestNack as e:
            print(f'Nacked with reason={e.reason}')
        except InterestTimeout:
            print(f'Timeout')
        except InterestCanceled:
            print(f'Canceled')
        except ValidationFailure:
            print(f'Data failed to validate')
        finally:
            data_name = service_name + Name.to_str(data_name)
            print(f'Put Data: {Name.to_str(data_name)}')
            app.put_data(data_name, content=content, freshness_period=10000)
            app.shutdown()

    name = Name.from_str(l[0])

    app.run_forever(after_start=main())



if __name__ == '__main__':
    receive_interest()
    send_interest()
