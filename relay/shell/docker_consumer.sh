nfd-start
ndnsec key-gen /root | ndnsec cert-install -
nfdc face create udp://relay.testNet
nfdc route add /ndn udp://relay.testNetrelay
nfdc route add prefix / nexthop udp://relay.testNet
