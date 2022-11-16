import cefpyco
import subprocess

prefix = 'ccnx:'
delimiter = '/'
seg_size = 1200
cache_time = 1000

def segment_content(_content):

    ### binary encode
    if type(_content) is not bytes:
        content = _content.encode(encoding='utf-8')
    else:
        content = _content

    cob = []

    content_size = len(content)
    num_seg = ((content_size -1) // seg_size) + 1

    for i in range(num_seg):
        offset = i * seg_size
        cob.insert(i, content[offset:offset + seg_size])

    return num_seg, cob

def put_content(cef_handler, interest_name, content):

    ### segmentation
    num_seg, cob = segment_content(content)

    print ("interest name: {}".format(interest_name))
    print ("number of segments {}".format(num_seg))

    for i in range(num_seg):
        print ("chunk num: {}".format(i))
        cef_handler.send_data(interest_name, cob[i], i, end_chunk_num=num_seg-1, expiry=cache_time, cache_time=cache_time)
    print ("complete send data")

def get_content_smi(cef_handler, interest_name):

    content = b''

    ### send symbolic interest
    cef_handler.send_symbolic_interest(interest_name)

    while True:

        info = cef_handler.receive()

        if info.is_data and (info.name == interest_name) and info.chunk_num != info.end_chunk_num:
            print ("end chunk num: {}".format(info.end_chunk_num))
            print ("chunk num: {}".format(info.chunk_num))
            content = content + info.payload
        elif info.is_data and (info.name == interest_name) and info.chunk_num == info.end_chunk_num:
            print ("end chunk num: {}".format(info.end_chunk_num))
            print ("chunk num: {}".format(info.chunk_num))
            content = content + info.payload
            break
        else:
            pass

    return content

def parse_interest(interest_name):

    ### interest model
    # ccnx:/<func>/<func>.../<data>
    mode = ''

    name_lists = interest_name.split(delimiter, 2)

    if len(name_lists) == 3:
        mode = 'service function mode'
    elif len(name_lists) == 2:
        mode = 'producer mode'
    else:
        print ('error: parse is failed')

    return mode, name_lists

def update_fib(fib_message):

    ARG = ['cefroute $0 $1 $2 $3',
           fib_message['method'],
           fib_message['uri'],
           fib_message['icn transport'],
           fib_message['ip']
          ]

    print (ARG)

    try:
        result = subprocess.Popen(ARG, shell=True, stdout=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        print ('error: {}'.format(e.stdout))
