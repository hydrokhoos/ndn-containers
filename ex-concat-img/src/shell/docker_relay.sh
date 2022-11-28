nfd-start
ndnsec key-gen /root | ndnsec cert-install -
nfdc face create udp://producer1.net
nfdc face create udp://producer2.net
nfdc face create udp://consumer.net
nfdc route add /ndn udp://producer1.net
nfdc route add /ndn udp://producer2.net
nfdc route add /ndn udp://consumer.net
nfdc route add prefix / nexthop udp://producer1.net
nfdc route add prefix / nexthop udp://producer2.net
nfdc route add prefix / nexthop udp://consumer.net

### zuru
nfdc route add prefix /img1.png nexthop udp://producer1.net
nfdc route add prefix /img2.png nexthop udp://producer2.net
nfdc route add prefix /img1.jpg nexthop udp://producer1.net
nfdc route add prefix /img2.jpg nexthop udp://producer2.net
