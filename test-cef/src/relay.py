import cefpyco
import json
import datetime
from queue import Queue

### own library
import cef_library as cef


def function_relay(data: bytes) -> bytes:
    return data


### set timezone
UTC = datetime.timezone.utc

### set queue size
queue_size = 10

### for logging
keep_alive = 60
###

### prefix name
prefix = 'ccnx:'
delimiter = '/'
service_name = 'relay'

def main_sidecar_thread():

    print ("start main sidecar thread")
    print ("service name: {}".format(service_name))

    ### delete special characters
    #_ccnx_name = ''.join(char for char in service_name if char.isalnum())
    #my_ccnx_name = prefix + delimiter + _ccnx_name
    my_ccnx_name = prefix + delimiter + service_name
    print ("my interest name: {}".format(my_ccnx_name))

    with cefpyco.create_handle() as handler:
        handler.register(my_ccnx_name)

        while True:
            info = handler.receive()

            print (info.name)

            ### receive the interest which contains my service name
            if info.is_symbolic_interest and my_ccnx_name in info.name:
                print (info)

                ### determine a next state
                mode, name_lists = cef.parse_interest(info.name)

                if mode == 'service function mode':

                    service_call_handler(handler, name_lists)

                elif mode == 'producer mode':
                    ### return content (no available)
                    pass

                else:
                    ### return error message (no available)
                    pass

            else:
                ### should be forwareded interest
                pass


def service_call_handler(cef_handler, name_lists):

    print ("start service call handler")

    ### get content
    interest_get_cob = prefix + delimiter + name_lists[2]
    print ("interest for get content {}".format(interest_get_cob))

    req_data = cef.get_content_smi(cef_handler, interest_get_cob)

    res_data = function_relay(req_data)

    ### set interest for put content
    interest_put_cob = prefix + delimiter + name_lists[1] + delimiter + name_lists[2]

    print ("interest for put content {}".format(interest_put_cob))

    ### put content
    cef.put_content(cef_handler, interest_put_cob, json.dumps(res_data))
    ###


if __name__ == '__main__':
    ### main sidecar thread
    main_sidecar_thread()
