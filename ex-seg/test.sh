./create.sh

docker exec consumer apt install iproute2 iputils-ping -y & \
docker exec producer apt install iproute2 -y
docker exec consumer tc qdisc add dev eth0 root netem delay 5ms
docker exec producer tc qdisc add dev eth0 root netem delay 5ms

docker exec consumer ping producer.net -c 10 > src/ping.txt

cd src/
python3 ../make_data.py
docker exec -d relay python3 /src/relay.py

echo "data size,consumer get time" > result.csv
for data in `ls -1 data*`
do
  echo -n "$data"
  echo "$data" > target_name
  docker exec -d producer python3 /src/producer.py
  sleep 1
  # docker exec consumer python3 /src/consumer.py
  docker exec consumer python3 /src/consumer_multi_thread.py
  diff $data fetched-*$data && echo -n " check OK"
  echo ""
done

mv result.csv ../result.csv -n
mv ping.txt ../ping.txt -n
rm data*
rm fetched-* -f
: > target_name

cd ..
python3 graph.py

./delete.sh
