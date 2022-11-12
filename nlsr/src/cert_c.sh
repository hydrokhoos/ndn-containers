# ルーターで、ルーター キーを生成します。
ndnsec-key-gen /ndn/test/%C1.Router/consumer > consumer.key

# ルーター キーをオペレーター サーバーにコピーし、ルーターの証明書を生成します。
ndnsec-cert-gen -s /ndn/test/%C1.Operator/op consumer.key > consumer.cert

# ルーター証明書をルーターにコピーしてインストールします。
ndnsec-cert-install -f consumer.cert
