# NLSRテスト

## コンテナイメージビルド
```bash
cd ndn-containers/nlsr/
sudo docker build . -t test-nlsr
```

## コンテナとネットワークの準備
```bash
./create.sh
```

## データの送信
### Producer
```bash
sudo docker exec -it producer bash
nfd-start
nfdc face create udp://consumer.testNet
nlsr -f /src/conf/producer/nlsr.conf
python3 /src/producer.py
```

### Consumer
```bash
sudo docker exec -it consumer bash
nfd-start
nfdc face create udp://producer.testNet
nlsr -f /src/conf/consumer/nlsr.conf
python3 /src/consumer.py
```

## コンテナとネットワークの削除
```bash
./delete.sh
```
