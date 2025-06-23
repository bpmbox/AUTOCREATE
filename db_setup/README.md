# db_setup/README.md

## 概要
このディレクトリは「Supabase(PostgreSQL)のテーブル自動作成・サンプルデータ投入・動作テスト」を安全に行うためのセットです。

- MCPや仮想DBは一切使いません
- .envのPOSTGRES接続情報を利用し、直接PostgreSQLに接続します
- 誰でも手順通りに実行するだけで、テーブル作成・サンプル投入・動作確認まで自動化できます

## 構成ファイル
- create_tables_postgres.py … テーブル作成・サンプルデータ投入・動作テスト一括スクリプト
- .env.example … 必要なPostgreSQL接続情報のサンプル

## 実行手順
1. `.env.example` をコピーして `.env` を作成し、実際の接続情報を記入してください
2. 必要なPythonパッケージをインストール
   ```
   pip install psycopg2-binary python-dotenv
   ```
3. スクリプトを実行
   ```
   python create_tables_postgres.py
   ```

## 注意
- 本番DBで実行する場合は、必ず接続情報を再確認してください
- 既存テーブルがあれば上書きせずスキップします
- サンプルデータが毎回追加されます

---

何か問題があれば管理者までご連絡ください。
