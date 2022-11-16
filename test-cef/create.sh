docker network create testnet
docker run -dit --name producer --net testnet -v $(pwd)/src/:/src/ test-cef
docker run -dit --name consumer --net testnet -v $(pwd)/src/:/src/ test-cef

docker
