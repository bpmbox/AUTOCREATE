# 🛠️ トラブルシューティングガイド

## 📋 よくある問題と解決策

### ❌ データベース関連エラー

#### 問題: `unable to open database file`

**発生状況**: GitHub Issue自動生成機能でのデータベースアクセスエラー

**エラーメッセージ例**:
```
❌ セットアップエラー: unable to open database file
```

#### 🔍 原因分析
1. **パス設定問題**: 古いプロジェクトパスが設定されている
2. **ファイル不存在**: 必要なデータベースファイルが作成されていない  
3. **権限問題**: データベースファイルへのアクセス権限不足

#### ✅ 解決手順

##### 1. データベースパス確認
```python
# config/database.py を確認
# 正しいパス: /workspaces/AUTOCREATE/database/
# 間違ったパス: /workspaces/fastapi_django_main_live/database/
```

##### 2. データベースファイル存在確認
```bash
ls -la database/
# 必要なファイル:
# - chat_history.db
# - github_issues.db  
# - approval_system.db
# - prompts.db
```

##### 3. データベース初期化
```bash
python database/init_databases.py
```

#### 📅 記録日時
- **発生日**: 2025年06月15日
- **状態**: 🔄 調査・修正中
- **報告者**: GitHub Copilot

---

### ⚡ Gradio関連エラー

#### 問題: キューエラー (`_queue` attribute error)

**エラーメッセージ例**:
```
AttributeError: 'TabbedInterface' object has no attribute '_queue'
```

#### ✅ 解決策
1. **段階的実装**: 動的ローダーではなく手動で1つずつ追加
2. **キュー初期化**: 各インターフェースのキューを適切に設定
3. **シンプルマウント**: `gr.mount_gradio_app()`を使用

#### 📅 記録日時
- **発生日**: 2025年06月15日
- **状態**: ✅ 解決済み（手動実装方式で回避）
- **解決者**: GitHub Copilot + miyataken999

---

## 🔧 一般的なデバッグ手順

### 1. ログ確認
```bash
# uvicornのログを確認
tail -f logs/app.log

# エラー詳細をキャッチ
python app.py --debug
```

### 2. データベース状態確認
```bash
# データベースファイル確認
find . -name "*.db" -type f

# 権限確認
ls -la database/
```

### 3. インポートエラー確認
```python
# 個別インポートテスト
try:
    from app.Http.Controllers.Gradio.gra_XX import gradio_interface
    print("✅ インポート成功")
except Exception as e:
    print(f"❌ インポートエラー: {e}")
```

## 📝 エラー報告テンプレート

新しいエラーを発見した場合は、以下のテンプレートを使用してこのドキュメントに追記してください：

```markdown
### ❌ [エラー名]

#### 問題: [簡潔な問題説明]

**発生状況**: [どこで、いつ発生したか]

**エラーメッセージ例**:
```
[実際のエラーメッセージ]
```

#### 🔍 原因分析
1. [原因1]
2. [原因2]

#### ✅ 解決手順
1. [解決手順1]
2. [解決手順2]

#### 📅 記録日時
- **発生日**: YYYY年MM月DD日
- **状態**: [調査中/解決済み/回避中]
- **報告者**: [GitHub Copilot/ユーザー名]
```

## 🔗 関連リンク
- [Gradioコンポーネント詳細ガイド](Gradio-Components-Guide.md)
- [開発ガイドライン](Development-Guidelines.md)
- [システムアーキテクチャ](System-Architecture.md)

---
**最終更新**: 2025年06月15日  
**管理者**: GitHub Copilot
