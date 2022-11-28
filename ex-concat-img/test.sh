docker exec -d producer1 python3 /src/producer1.py
docker exec -d producer2 python3 /src/producer2.py
docker exec -d relay python3 /src/concatimg.py

sleep 60
docker exec consumer python3 /src/consumer.py

cd src/ && ./concat.sh && cd ..
python3 ts_show.py
cp src/fetched-* .

./delete.sh
