# 🔥 GitHub Copilot 完全自動回答システム

## ✨ 概要
Supabaseの`chat_history`テーブルを監視し、新しいユーザー質問を自動でGitHub Copilotチャットに投稿する完全自動システムです。

## 🚀 特徴
- **完全自動化**: 手を離して永続実行可能
- **OpenAI API不要**: GitHub Copilotが直接回答
- **リアルタイム監視**: 3秒間隔でSupabaseをチェック
- **Copilotフィルタ**: AI/Botメッセージは自動除外
- **固定座標**: 座標設定済みで即座に開始

## 📋 完全自動起動方法

### 方法1: バッチファイル (Windows)
```bash
# ダブルクリックまたはコマンドプロンプトから
start_auto_copilot.bat
```

### 方法2: PowerShell
```powershell
# PowerShellから
.\start_auto_copilot.ps1
```

### 方法3: 直接実行
```bash
cd tests/Feature
python copilot_direct_answer.py --auto
```

## 🛠️ 手動設定モード
```bash
cd tests/Feature
python copilot_direct_answer.py
```

### メニューオプション:
- `1`: 📍 チャット座標記録
- `5`: 🔄 高性能自動監視モード
- `8`: 🔥 無限自動ループ
- `9`: ⚡ クイック自動開始

## ⚙️ システム要件

### 必要パッケージ:
```bash
pip install -r requirements_supabase_chat.txt
```

### 環境設定 (.env):
```env
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
```

## 🔧 動作フロー

1. **監視開始**: Supabaseの`chat_history`テーブルを3秒間隔でチェック
2. **新着検出**: Copilot以外のユーザーからの新しいメッセージを検出
3. **自動転送**: VS Code Copilotチャットに質問を自動投稿
4. **直接回答**: GitHub Copilotが直接回答を提供
5. **処理済みマーク**: 処理済みフラグを自動設定

## 🎯 固定座標設定
- **X座標**: 1335
- **Y座標**: 1045
- VS Code Copilotチャットの入力欄を想定

## ⚠️ 注意事項

- VS Code Copilotチャットを事前に開いておく
- チャット入力欄が座標位置にあることを確認
- 完全自動モードでは手動操作不要
- Ctrl+C で停止

## 🔥 推奨使用法

**完全自動永続実行**:
```bash
start_auto_copilot.bat
```

これで手を離して永続的にSupabaseの質問を監視し、自動でCopilotに転送されます！

## 📊 システム構成

```
AUTOCREATE/
├── tests/Feature/
│   └── copilot_direct_answer.py  # メインスクリプト
├── requirements_supabase_chat.txt # 依存パッケージ
├── start_auto_copilot.bat        # Windows起動用
├── start_auto_copilot.ps1        # PowerShell起動用
├── .env                          # Supabase設定
└── chat_coordinates.json         # チャット座標(自動生成)
```

## ✅ 完了状態

✅ **Supabaseリアルタイム監視**  
✅ **完全自動質問転送**  
✅ **Copilotフィルタリング**  
✅ **固定座標設定**  
✅ **永続実行モード**  
✅ **ヘッドレス起動**  
✅ **エラーハンドリング**  

🎉 **システム完成！手を離して永続実行可能**
