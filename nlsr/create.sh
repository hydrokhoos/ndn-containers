echo 'Creating network ...'
sudo docker network create testNet
echo ''

echo 'Running containers ...'
sudo docker run -dit --name producer --net testNet --privileged -v $(pwd)/src/:/src hydrokhoos/test-nlsr
sudo docker run -dit --name consumer --net testNet --privileged -v $(pwd)/src/:/src hydrokhoos/test-nlsr
echo ''

echo 'Configuring security ...'
sudo docker exec producer bash /src/cert_p.sh
sudo docker cp producer:/root.cert root.cert
sudo docker cp producer:/site.cert site.cert
sudo docker cp root.cert consumer:/root.cert
sudo docker cp site.cert consumer:/site.cert
rm root.cert site.cert -f
sudo docker exec producer bash /src/cert_c.sh
echo ''

# echo 'Starting NFD ...'
# sudo docker exec producer nfd-start;
# sudo docker exec producer nfdc face create udp://consumer.testNet;
# sudo docker exec producer nlsr -f /src/conf/producer.conf;
# sudo docker exec consumer nfd-start;
# sudo docker exec consumer nfdc face create udp://producer.testNet;
# sudo docker exec consumer nlsr -f /src/conf/consumer.conf;
# echo ''

echo 'Created'
