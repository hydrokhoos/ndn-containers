# ルート サーバーで、ルート キーを生成します。
ndnsec-key-gen /ndn/ > root.key

# ルート サーバーでルート キーの証明書を生成します。
ndnsec-cert-dump -i /ndn/ > root.cert

# ルート サーバーにルート証明書をインストールします。
ndnsec-cert-install -f root.cert

# サイト サーバーで、サイト キーを生成します。
ndnsec-key-gen /ndn/test > site.key

# サイト キーをルート サーバーにコピーし、サイト サーバーの証明書を生成します。
ndnsec-cert-gen -s /ndn/ site.key > site.cert

# サイト証明書をサイト サーバーにコピーしてインストールします。
ndnsec-cert-install -f site.cert

# オペレーター サーバーで、オペレーター キーを生成します。
ndnsec-key-gen /ndn/test/%C1.Operator/op > op.key

# オペレーター キーをサイト サーバーにコピーし、オペレーター サーバーの証明書を生成します。
ndnsec-cert-gen -s /ndn/test op.key > op.cert

# オペレーター証明書をオペレーター サーバーにコピーしてインストールします。
ndnsec-cert-install -f op.cert

# ルーターで、ルーター キーを生成します。
ndnsec-key-gen /ndn/test/%C1.Router/producer > producer.key

# ルーター キーをオペレーター サーバーにコピーし、ルーターの証明書を生成します。
ndnsec-cert-gen -s /ndn/test/%C1.Operator/op producer.key > producer.cert

# ルーター証明書をルーターにコピーしてインストールします。
ndnsec-cert-install -f producer.cert
