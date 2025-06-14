# 🛠️ 開発ガイドライン - Laravel風アーキテクチャ統一

## 🎯 プロジェクト目標

**Laravel風の構成に統一して、開発者参加を容易にする**

> Laravel経験者なら説明不要で参加できる構造を目指す

## 🏗️ アーキテクチャ変更計画

### 📁 現在の課題
- `mysite/asgi.py` にルーティング処理が混在
- Laravel風構造が不完全
- 開発者にとって特殊な説明が必要

### 🎯 目標構成 (Laravel準拠)

```
📁 プロジェクト構造
├── routes/
│   ├── web.py           ← 全WebルーティングをここにAGGURIGATE
│   ├── api.py           ← API専用ルーティング
│   └── gradio.py        ← Gradio専用ルーティング
├── app/Http/Controllers/
│   ├── WebController.py     ← Web画面処理
│   ├── GradioController.py  ← Gradio統合処理
│   └── ApiController.py     ← API処理
├── mysite/
│   └── asgi.py          ← アプリケーション起動のみ (ルーティング除去)
└── controllers/         ← 機能別コントローラー (現在のまま)
```

## 🔄 移行ステップ

### Step 1: 設計・計画
1. **Wikiドキュメント作成** ✅ (このページ)
2. **GitHub Issue作成** 
3. **テストケース設計**

### Step 2: 自動テスト実装
1. **Artisanコマンド拡張**
   ```bash
   python artisan test:routing    # ルーティングテスト
   python artisan test:gradio     # Gradio統合テスト  
   python artisan test:laravel    # Laravel構造テスト
   ```

2. **テストケース追加**
   - 全ルートの動作確認
   - Gradio個別アクセステスト
   - 統合ダッシュボードテスト

### Step 3: コード移行
1. **routes/web.py 拡張**
   - `asgi.py` からルーティング移行
   - 個別Gradio `/gradio/{機能名}` ルート追加
   - 統合ダッシュボード `/gradio/dashboard` 追加

2. **Controllers 強化**
   - Laravel風Controller完全実装
   - Gradio自動検出・マウント機能

3. **asgi.py 簡素化**
   - ルーティング処理を完全除去
   - アプリケーション初期化のみに特化

### Step 4: CI/CD統合
1. **GitHub Actions設定**
   ```yaml
   name: Laravel-Style Architecture Test
   on: [push, pull_request]
   jobs:
     test:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v3
         - name: Setup Python
         - name: Install dependencies
         - name: Run Laravel Structure Tests
           run: python artisan test:all
         - name: Run Gradio Integration Tests
           run: python artisan test:gradio
   ```

## 🎯 期待される効果

### 👨‍💻 開発者参加の容易化
- **Laravel経験者**: 即座に理解・参加可能
- **新規開発者**: Laravel資料で学習可能
- **AI協働**: Laravel標準パターンで指示可能

### 📚 ドキュメント簡素化
- **特殊な説明不要**: Laravel標準説明で十分
- **学習コスト削減**: 既存知識で理解可能
- **保守性向上**: 一般的なパターンで保守容易

### 🔧 開発効率向上
- **ルーティング一元化**: `routes/web.py` で全体把握
- **責務分離**: 各ファイルの役割明確化
- **テスト容易化**: 標準的なテスト手法適用可能

## 🧪 テスト戦略

### 📋 テストケース設計

#### 1. ルーティングテスト
```python
def test_individual_gradio_routes():
    """個別Gradioルートの動作確認"""
    routes = [
        "/gradio/chat",
        "/gradio/database", 
        "/gradio/files",
        "/gradio/github"
    ]
    for route in routes:
        response = client.get(route)
        assert response.status_code == 200

def test_unified_dashboard():
    """統合ダッシュボードテスト"""
    response = client.get("/gradio/dashboard")
    assert response.status_code == 200
    assert "統合ダッシュボード" in response.text
```

#### 2. Controller統合テスト
```python  
def test_gradio_auto_discovery():
    """Gradio自動検出機能テスト"""
    from app.Http.Controllers.GradioController import discover_gradio_interfaces
    interfaces = discover_gradio_interfaces()
    assert len(interfaces) > 0
    assert all(hasattr(interface, 'gradio_interface') for interface in interfaces)
```

#### 3. Laravel構造テスト
```python
def test_laravel_structure_compliance():
    """Laravel構造準拠テスト"""
    # 必要なディレクトリ存在確認
    assert os.path.exists("routes/web.py")
    assert os.path.exists("app/Http/Controllers/")
    
    # ルーティング分離確認
    with open("mysite/asgi.py") as f:
        content = f.read()
        assert "@app.get" not in content  # ルーティングがないことを確認
```

## 🔧 Artisanコマンド拡張

### 新規追加コマンド

```bash
# テスト実行
python artisan test:routing     # ルーティングテスト
python artisan test:gradio      # Gradio統合テスト
python artisan test:laravel     # Laravel構造準拠テスト  
python artisan test:all         # 全テスト実行

# 開発支援
python artisan make:controller WebController    # Controller生成
python artisan make:route gradio               # ルート生成
python artisan route:list                      # ルート一覧表示

# 構造確認
python artisan structure:check    # Laravel構造確認
python artisan gradio:list        # Gradio機能一覧
```

## 📊 成功指標

### ✅ 完了条件
1. **全テストPASS**: 自動テストで100% PASS
2. **GitHub Actions**: CI/CDでテスト成功  
3. **構造準拠**: Laravel標準構造完全準拠
4. **機能維持**: 既存機能の完全動作保証

### 📈 改善指標
- **開発者参加時間**: 30分以内でプロジェクト理解
- **新機能追加時間**: 従来の50%時間短縮
- **保守作業効率**: 問題特定・修正時間半減

## 🚀 実装スケジュール

### Week 1: 設計・テスト準備
- [x] Wikiドキュメント作成
- [ ] GitHub Issue作成  
- [ ] テストケース設計
- [ ] Artisanコマンド実装

### Week 2: コード移行
- [ ] routes/web.py 拡張
- [ ] Controller実装
- [ ] asgi.py 簡素化
- [ ] テスト実行・修正

### Week 3: CI/CD・最終テスト
- [ ] GitHub Actions設定
- [ ] 統合テスト
- [ ] ドキュメント更新
- [ ] リリース

---

**作成者**: miyataken999 + GitHub Copilot  
**作成日**: 2025年06月14日  
**ステータス**: 🚧 計画中 → 実装準備

> 🎯 **Laravel経験者なら即参加可能な、わかりやすいアーキテクチャを目指します**
