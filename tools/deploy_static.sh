#!/usr/bin/env bash
# Basit dağıtım aracı: yerel `static/images/` ve `static/uploads/` klasörlerini uzak sunucuya rsync ile kopyalar
# Kullanım: ./tools/deploy_static.sh user@host [remote_path]
# Örnek: ./tools/deploy_static.sh ubuntu@1.2.3.4 ~/GaziantepLezzetRehberi.io

set -euo pipefail

REMOTE=${1:-}
REMOTE_PATH=${2:-~/GaziantepLezzetRehberi.io}

if [ -z "$REMOTE" ]; then
  echo "Kullanım: $0 user@host [remote_path]"
  exit 2
fi

echo "Hedef: $REMOTE : $REMOTE_PATH"

echo "Uzak dizinleri oluşturuyorum..."
ssh "$REMOTE" "mkdir -p $REMOTE_PATH/static/images $REMOTE_PATH/static/uploads"

echo
echo "=== DRY-RUN: static/images ==="
rsync -avz --progress --dry-run static/images/ "$REMOTE:$REMOTE_PATH/static/images/"
echo
echo "=== DRY-RUN: static/uploads ==="
rsync -avz --progress --dry-run static/uploads/ "$REMOTE:$REMOTE_PATH/static/uploads/"

read -p "Dry-run sonuçlarını gördünüz mü? Gerçek kopyalama yapılsın mı? (y/N): " CONF
if [[ "$CONF" != "y" && "$CONF" != "Y" ]]; then
  echo "İptal edildi. Dry-run sonuçlarını kontrol edip tekrar çalıştırın.";
  exit 0
fi

echo "Gerçek kopyalama başlıyor..."
rsync -avz --progress static/images/ "$REMOTE:$REMOTE_PATH/static/images/"
rsync -avz --progress static/uploads/ "$REMOTE:$REMOTE_PATH/static/uploads/"

echo "Kopyalama tamamlandı. Uzak sunucuda fix scripti çalıştırmak isterseniz şu komutu kullanın:"
echo
echo "ssh $REMOTE 'cd $REMOTE_PATH && chmod +x tools/fix_server.sh && sudo bash tools/fix_server.sh'"
echo
echo "Not: Bu script sizin yerel makinenizde çalıştırılmak içindir. Ben doğrudan sunucuya bağlanamam; lütfen bu script'i kendi terminalinizde çalıştırın."
