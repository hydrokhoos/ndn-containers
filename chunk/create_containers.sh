sudo docker network create testNet
sudo docker run -dit --name consumer --net testNet --privileged -v /home/$(whoami)/ndn-containers/chunk/:/chunk hydrokhoos/ubuntu-ndn-python
sudo docker run -dit --name producer --net testNet --privileged -v /home/$(whoami)/ndn-containers/chunk/:/chunk hydrokhoos/ubuntu-ndn-python

sudo docker network inspect testNet

sudo docker cp ./exec_producer.sh producer:/
sudo docker exec producer bash ./exec_producer.sh
sudo docker cp ./exec_consumer.sh consumer:/
sudo docker exec consumer bash ./exec_consumer.sh
