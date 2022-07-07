# Relay (仮)

## コンテナ・ネットワークの準備
```bash
cd ndn-containers/relay
./create_containers.sh
```

## メッセージ(Hello, world!)の送信
### Producer
コンテナに入って、```producer.py```を実行
```bash
sudo docker exec -it producer bash
python3 /relay/producer.py
```

### Relay
コンテナに入って、```relay.py```を実行
```bash
sudo docker exec -it relay bash
python3 /relay/relay.py
```

### Consumer
コンテナに入って、```consumer.py```を実行
```bash
sudo docker exec -it consumer bash
python3 /relay/consumer.py
```

## コンテナ・ネットワークの削除
```bash
./delete_containers.sh
```
