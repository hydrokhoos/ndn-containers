nfd-start
ndnsec key-gen /root | ndnsec cert-install -
nfdc face create udp://producer.net
nfdc face create udp://consumer.net
nfdc route add /ndn udp://producer.net
nfdc route add /ndn udp://consumer.net
nfdc route add prefix / nexthop udp://producer.net
nfdc route add prefix / nexthop udp://consumer.net
