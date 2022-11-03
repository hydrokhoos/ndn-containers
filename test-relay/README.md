# relay

## コンテナ・ネットワークの準備
```bash
cd ndn-containers/test-chunk
./create_containers.sh
```

## データ(abc...xyz)の送信
### Producer
コンテナに入って、put3chunks.pyを実行
```bash
sudo docker exec -it producer bash
python3 /test-chunk/put3chunks.py
```
### Relay(123...789を追加)
コンテナに入って、relay-thread.pyを実行
```bash
sudo docker exec -it relay bash
python3 /test-chunk/relay-thread.py
```

### Consumer
コンテナに入って、getchunks.pyを実行
```bash
sudo docker exec -it consumer bash
python3 /chunk/getchunks.py
```

## コンテナ・ネットワークの削除
```bash
./delete_containers.sh
```
