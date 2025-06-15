# AUTOCREATE株式会社 - GitHub Issues & Project Management

## 🏷️ ラベル戦略

### プロジェクト管理用ラベル

#### 🚀 タスク種別
- `task` - 一般的なタスク（青色 #0052CC）
- `enhancement` - 機能強化（緑色 #00FF00）
- `bug` - バグ修正（赤色 #FF0000）
- `documentation` - ドキュメント整備（黄色 #FFFF00）

#### 🎯 優先度
- `priority:high` - 高優先度（濃い赤 #B60205）
- `priority:medium` - 中優先度（オレンジ #FF8C00）
- `priority:low` - 低優先度（薄い灰色 #D1D3D4）

#### 🏛️ AUTOCREATE専用
- `ai-ceo` - AI社長関連（紫色 #9F4CFF）
- `cto-jobless` - 無職CTO関連（水色 #00BFFF）
- `ocr-rpa` - OCR+RPA関連（緑色 #32CD32）
- `kinkaimasu` - kinkaimasu.jp案件（金色 #FFD700）

#### 🌍 業界・展開
- `reuse-industry` - リユース業界（茶色 #8B4513）
- `automation` - 自動化関連（濃い青 #000080）
- `business-proposal` - ビジネス提案（濃い緑 #006400）

#### 📱 技術スタック
- `gas-api` - Google Apps Script（赤色 #EA4335）
- `python` - Python関連（青色 #306998）
- `docker` - Docker関連（青色 #2496ED）
- `jupyter` - Jupyter Notebook（オレンジ #F37626）

## 📋 Issue テンプレート

### 1. タスクIssue
```markdown
## 🎯 タスク概要
[タスクの簡潔な説明]

## 🏛️ AI社長×無職CTO体制での役割分担
- **AI社長**: [戦略・企画・顧客対応]
- **無職CTO**: [技術実装・システム構築]

## 📝 実装内容
- [ ] [具体的な作業項目1]
- [ ] [具体的な作業項目2]
- [ ] [具体的な作業項目3]

## 🎯 完了条件
- [ ] [完了条件1]
- [ ] [完了条件2]

## 💰 ビジネス価値
[このタスクが創出するビジネス価値]

## 📅 期限
[予定完了日]
```

### 2. 機能強化Issue
```markdown
## 🚀 機能強化概要
[機能強化の説明]

## 💡 現状の課題
[解決したい課題]

## 🎯 期待される効果
[機能強化による効果]

## 🔧 技術的要件
- [ ] [技術要件1]
- [ ] [技術要件2]

## 🏆 成功指標
[成功を判断する指標]
```

### 3. kinkaimasu.jp案件Issue
```markdown
## 🏪 kinkaimasu.jp案件

### 🎯 案件概要
[案件の説明]

### 💰 想定ROI
- **売上向上**: [金額]
- **コスト削減**: [金額]
- **効率化**: [パーセンテージ]

### 🔄 自動化対象
- [ ] [自動化項目1]
- [ ] [自動化項目2]

### 📊 競合分析
[競合他社との比較・優位性]

### 🎁 0円提案内容
[無料テスト導入の内容]
```

## 🏗️ プロジェクト構造

### Project: AUTOCREATE
- **View**: Board形式
- **Columns**: 
  - 📝 Backlog
  - 🚀 In Progress  
  - 🔍 Review
  - ✅ Done
  - 🎯 Deployed

### 自動化ルール
- `priority:high`ラベルのIssue → 自動的に"In Progress"に移動
- `kinkaimasu`ラベルのIssue → AI社長にアサイン
- `ocr-rpa`ラベルのIssue → 無職CTOにアサイン
