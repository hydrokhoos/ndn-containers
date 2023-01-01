import time
import random


SEGMENT_SIZE = 4000

data = random.randbytes(30 * 1024 * 1024)
num_seg = (len(data) + SEGMENT_SIZE - 1) // SEGMENT_SIZE

t = time.time()
data_list = [data[i*SEGMENT_SIZE:(i+1)*SEGMENT_SIZE] for i in range(num_seg)]
print(len(data_list) == num_seg)
print(time.time() - t)
