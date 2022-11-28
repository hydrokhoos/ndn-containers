echo 'Creating network; net'
docker network create net
echo 'Running containers; consumer, relay, producer1 producer2'
docker run -dit --name consumer --net net --privileged -v $(pwd)/src/:/src hydrokhoos/ubuntu-ndn-python
docker run -dit --name relay --net net --privileged -v $(pwd)/src/:/src hydrokhoos/ubuntu-ndn-python
docker run -dit --name producer1 --net net --privileged -v $(pwd)/src/:/src hydrokhoos/ubuntu-ndn-python
docker run -dit --name producer2 --net net --privileged -v $(pwd)/src/:/src hydrokhoos/ubuntu-ndn-python

sleep 1
docker exec relay pip install Pillow


### consumer---relay-+-producer1 ###
###                  +-producer2 ###
echo 'Initiating producer ...'
docker exec producer1 bash /src/shell/docker_producer.sh
docker exec producer2 bash /src/shell/docker_producer.sh
echo 'Initiating relay ...'
docker exec relay bash /src/shell/docker_relay.sh
echo 'Initiating consumer ...'
docker exec consumer bash /src/shell/docker_consumer.sh

echo "Creating log files ..."
echo "time,action,name,segment number" > src/consumer.csv
echo "time,action,name,segment number" > src/relay.csv
echo "time,action,name,segment number" > src/producer1.csv
echo "time,action,name,segment number" > src/producer2.csv

echo -e '\nCreated'
