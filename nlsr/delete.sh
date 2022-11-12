echo 'Stopping containers ...'
sudo docker stop consumer producer

echo 'Removeing containers ...'
sudo docker container rm consumer producer

echo 'Removing network ...'
sudo docker network rm testNet

echo -e '\nDeleted'
