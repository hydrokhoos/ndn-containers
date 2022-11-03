# with open('/test-relay/log.txt') as f:
with open('log.txt') as f:
    p = float(f.readline().strip())
    c = float(f.readline().strip())

end2end = c - p

# print(end2end)

with open('summary.txt', 'a') as f:
    f.write(str(end2end))
    f.write('\n')
