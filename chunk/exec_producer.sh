nfd-start
nfdc face create udp://consumer.testNet
nfdc route add /ndn udp://consumer.testNet
ndnsec key-gen /$(whoami) | ndnsec cert-install -
nfdc route add prefix / nexthop udp://consumer.testNet
