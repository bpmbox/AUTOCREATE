<?php
// php_batch_sample.php
// シンプルなPHPバッチ処理サンプル

echo "バッチ処理開始\n";
for ($i = 1; $i <= 5; $i++) {
    echo "処理中: $i\n";
    sleep(1);
}
echo "バッチ処理終了\n";
