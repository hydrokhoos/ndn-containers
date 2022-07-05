# get/putchunks-test

## コンテナ・ネットワークの準備
```bash
cd ndn-containers/chunk
./create_containers.sh
```

## 画像の送信
### Producer
コンテナに入って、putchunks-test.pyを実行
```bash
sudo docker exec -it producer bash
python3 /chunk/putchunks-test.py theta /chunk/theta.jpg
```
```
Created 791 chunks under name /theta/v=1656349826923
```

### Consumer
コンテナに入って、getchunks-test.pyを実行
```bash
sudo docker exec -it consumer bash
python3 /chunk/getchunks-test.py /theta/v=1656349826923
```

## 画像の確認
```ndn-containers/chunk/fetch_data.jpg```

## コンテナ・ネットワークの削除
```bash
./delete_containers.sh
```

## ログ
```log.csv```に保存

サマリ(```summary.csv```)の出力
```bash
python3 analyze_log.py
```

```bash
sudo ./clear_log.sh
```

## fetch_data.jpg, log.csv, summary.csv初期化
```bash
./init.sh
```
