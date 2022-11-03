echo 'Creating network; testNet'
sudo docker network create testNet
echo 'Running containers; consumer, relay, producer'
sudo docker run -dit --name consumer --net testNet --privileged -v $(pwd):/test-relay hydrokhoos/ubuntu-ndn-python
sudo docker run -dit --name relay --net testNet --privileged -v $(pwd):/test-relay hydrokhoos/ubuntu-ndn-python
sudo docker run -dit --name producer --net testNet --privileged -v $(pwd):/test-relay hydrokhoos/ubuntu-ndn-python


### consumer---relay---producer ###
echo 'Initiating producer ...'
sudo docker exec producer bash /test-relay/shell/docker_producer.sh
echo 'Initiating relay ...'
sudo docker exec relay bash /test-relay/shell/docker_relay.sh
echo 'Initiating consumer ...'
sudo docker exec consumer bash /test-relay/shell/docker_consumer.sh

echo -e '\nCreated'
