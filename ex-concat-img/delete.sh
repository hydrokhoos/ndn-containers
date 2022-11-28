echo 'Stopping containers ...'
docker stop consumer producer1 producer2 relay

echo 'Removeing containers ...'
docker container rm consumer producer1 producer2 relay

echo 'Removing network ...'
docker network rm net

echo "Removing files ..."
rm src/*.csv src/fetched-* -f

echo -e '\nDeleted'
