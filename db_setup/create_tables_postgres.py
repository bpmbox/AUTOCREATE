import os
from dotenv import load_dotenv
import psycopg2

# .envから環境変数をロード
env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(env_path)

POSTGRES_URL = os.getenv('POSTGRES_URL')

# テーブル定義
CREATE_PROMPT_TABLE = '''
CREATE TABLE IF NOT EXISTS prompt (
    id SERIAL PRIMARY KEY,
    prompt_text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
'''

CREATE_DOCUMENTATION_TABLE = '''
CREATE TABLE IF NOT EXISTS documentation (
    id SERIAL PRIMARY KEY,
    doc_title VARCHAR(255) NOT NULL,
    doc_content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
'''

def main():
    try:
        conn = psycopg2.connect(POSTGRES_URL)
        conn.autocommit = True
        cur = conn.cursor()
        print('Connected to PostgreSQL.')

        print('Creating prompt table...')
        cur.execute(CREATE_PROMPT_TABLE)
        print('prompt table created or already exists.')

        print('Creating documentation table...')
        cur.execute(CREATE_DOCUMENTATION_TABLE)
        print('documentation table created or already exists.')

        # サンプルプロンプトを挿入
        sample_prompt = "これはサンプルプロンプトです。"
        cur.execute("INSERT INTO prompt (prompt_text) VALUES (%s) RETURNING id;", (sample_prompt,))
        inserted_id = cur.fetchone()[0]
        print(f'Sample prompt inserted with id: {inserted_id}')

        # promptテーブルからデータ取得して表示
        cur.execute("SELECT id, prompt_text, created_at FROM prompt ORDER BY id DESC LIMIT 5;")
        rows = cur.fetchall()
        print('Latest prompt data:')
        for row in rows:
            print(row)

        # サンプルドキュメントを挿入
        sample_doc_title = "サンプルまとめタイトル"
        sample_doc_content = "これはdocumentationテーブルへのサンプルまとめ内容です。"
        cur.execute(
            "INSERT INTO documentation (doc_title, doc_content) VALUES (%s, %s) RETURNING id;",
            (sample_doc_title, sample_doc_content)
        )
        doc_inserted_id = cur.fetchone()[0]
        print(f'Sample documentation inserted with id: {doc_inserted_id}')

        # documentationテーブルからデータ取得して表示
        cur.execute("SELECT id, doc_title, doc_content, created_at FROM documentation ORDER BY id DESC LIMIT 5;")
        doc_rows = cur.fetchall()
        print('Latest documentation data:')
        for row in doc_rows:
            print(row)

        cur.close()
        conn.close()
        print('Done.')
    except Exception as e:
        print(f'Error: {e}')

if __name__ == '__main__':
    main()
