./create.sh

# docker exec consumer apt install iproute2 iputils-ping -y & \
# docker exec producer apt install iproute2 -y & \
# docker exec relay apt install iproute2 -y ;
# sleep 1
# docker exec consumer tc qdisc add dev eth0 root netem delay 5ms
# docker exec producer tc qdisc add dev eth0 root netem delay 5ms
# docker exec relay tc qdisc add dev eth0 root netem delay 3ms

# docker exec consumer ping producer.net -c 10 > src/ping.txt

cd src/
python3 ../make_data.py
docker exec -d relay python3 /src/relay.py

echo "data size,consumer get time" > cgettime
for data in `ls -1 data*`
do
  echo "time,action,name,segment number" > consumer.csv
  echo "time,action,name,segment number" > relay.csv
  echo "time,action,name,segment number" > producer.csv

  echo -n "$data"
  echo "$data" > target_name
  docker exec -d producer python3 /src/producer.py
  sleep 3
  docker exec consumer python3 /src/consumer.py
  diff $data fetched-*$data && echo -n " check OK"
  echo ""
  ./concat.sh
  cd ../ && python3 ts_show.py && cd src/
  rm result.csv
done

mv ping.txt ../ping.txt
mv cgettime ../cgettime.csv
rm data*
: > target_name

cd ..
python3 graph.py
# python3 graph-pts.py

./delete.sh
