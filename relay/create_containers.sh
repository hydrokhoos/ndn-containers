echo 'Creating network; testNet'
sudo docker network create testNet
echo 'Running containers; consumer, relay, producer'
sudo docker run -dit --name consumer --net testNet --privileged -v $(pwd):/relay hydrokhoos/ubuntu-ndn-python
sudo docker run -dit --name relay --net testNet --privileged -v $(pwd):/relay hydrokhoos/ubuntu-ndn-python
sudo docker run -dit --name producer --net testNet --privileged -v $(pwd):/relay hydrokhoos/ubuntu-ndn-python


### consumer---relay---producer ###
echo 'Initiating producer ...'
sudo docker exec producer nfd-start
# sudo docker exec producer ndnsec key-gen /$(whoami) | ndnsec cert-install -
sudo docker exec producer nfdc face create udp://relay.testNet
sudo docker exec producer nfdc route add /ndn udp://relay.testNet
sudo docker exec producer nfdc route add prefix / nexthop udp://relay.testNet
echo 'Initiating relay ...'
sudo docker exec relay nfd-start
# sudo docker exec relay ndnsec key-gen /$(whoami) | ndnsec cert-install -
sudo docker exec relay nfdc face create udp://producer.testNet
sudo docker exec relay nfdc face create udp://consumer.testNet
sudo docker exec relay nfdc route add /ndn udp://producer.testNet
sudo docker exec relay nfdc route add /ndn udp://consumer.testNet
sudo docker exec relay nfdc route add prefix / nexthop udp://producer.testNet
sudo docker exec relay nfdc route add prefix / nexthop udp://consumer.testNet
echo 'Initiating consumer ...'
sudo docker exec consumer nfd-start
# sudo docker exec consumer ndnsec key-gen /$(whoami) | ndnsec cert-install -
sudo docker exec consumer nfdc face create udp://relay.testNet
sudo docker exec consumer nfdc route add /ndn udp://relay.testNetrelay
sudo docker exec consumer nfdc route add prefix / nexthop udp://relay.testNet

echo -e '\nCreated'
