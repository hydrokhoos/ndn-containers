nfd-start
ndnsec key-gen /root | ndnsec cert-install -
nfdc face create udp://producer.testNet
nfdc face create udp://consumer.testNet
nfdc route add /ndn udp://producer.testNet
nfdc route add /ndn udp://consumer.testNet
nfdc route add prefix / nexthop udp://producer.testNet
nfdc route add prefix / nexthop udp://consumer.testNet
