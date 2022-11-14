echo 'Creating network; net'
sudo docker network create net
echo 'Running containers; consumer, relay, producer'
sudo docker run -dit --name consumer --net net --privileged -v $(pwd)/src/:/src hydrokhoos/ubuntu-ndn-python
sudo docker run -dit --name relay --net net --privileged -v $(pwd)/src/:/src hydrokhoos/ubuntu-ndn-python
sudo docker run -dit --name producer --net net --privileged -v $(pwd)/src/:/src hydrokhoos/ubuntu-ndn-python


### consumer---relay---producer ###
echo 'Initiating producer ...'
sudo docker exec producer bash /src/shell/docker_producer.sh
echo 'Initiating relay ...'
sudo docker exec relay bash /src/shell/docker_relay.sh
echo 'Initiating consumer ...'
sudo docker exec consumer bash /src/shell/docker_consumer.sh

echo -e '\nCreated'
