nfd-start
ndnsec key-gen /root | ndnsec cert-install -
nfdc face create udp://relay.net
nfdc route add /ndn udp://relay.net
nfdc route add prefix / nexthop udp://relay.net
