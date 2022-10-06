echo 'Stopping containers ...'
sudo docker stop consumer producer relay

echo 'Removeing containers ...'
sudo docker container rm consumer producer relay

echo 'Removing network ...'
sudo docker network rm testNet

echo -e '\nDeleted'
