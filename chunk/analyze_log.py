import csv


header = ['time', 'from', 'number', 'size', 'name']
with open('log.csv', 'r') as f:
    reader = csv.DictReader(f, header)
    l = [row for row in reader]

max = 0
for item in l:
    if int(item['number']) > max:
        max = int(item['number'])
else:
    max += 1

summary = []
for i in range(max):
    p_l_search = [item for item in l if int(item['number']) == i and item['from'] == 'producer']
    c_l_search = [item for item in l if int(item['number']) == i and item['from'] == 'consumer']

    put_time = float(p_l_search[0]['time'])
    get_time = float(c_l_search[0]['time'])
    # msec
    latency = (get_time - put_time) * 1000

    packet_size = int(p_l_search[0]['size'])
    segment_size = int(c_l_search[0]['size'])
    header_size = packet_size - segment_size
    # Mbps
    trans_speed = packet_size / latency * 8 / 1000

    summary.append({'number': i,
                    'latency': latency,
                    'packet size': packet_size,
                    'segment size': segment_size,
                    'header size': header_size,
                    'trans speed': trans_speed})

with open('summary.csv', 'w') as f:
    writer = csv.DictWriter(f, ['number', 'latency', 'packet size', 'segment size', 'header size', 'trans speed'])
    writer.writeheader()
    writer.writerows(summary)
