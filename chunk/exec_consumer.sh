nfd-start
nfdc face create udp://producer.testNet
nfdc route add /ndn udp://producer.testNet
ndnsec key-gen /$(whoami) | ndnsec cert-install -
nfdc route add prefix / nexthop udp://producer.testNet
