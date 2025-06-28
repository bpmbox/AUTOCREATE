#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ナレッジ連動システムテスト
GitHub Copilot自動開発パイプラインのテスト実行
"""

import os
import json
from datetime import datetime
from pathlib import Path

def test_knowledge_auto_generation():
    """ナレッジ自動生成のテスト"""
    print("🧪 ナレッジ自動生成システムテスト開始")
    print("=" * 50)
    
    # テスト用の質問データ
    test_question = {
        'id': 9999,
        'question': 'React TypeScript プロジェクトでのAPI統合のベストプラクティスは？',
        'user': 'test-user',
        'created': datetime.now().isoformat()
    }
    
    # テスト用のCopilot回答
    test_response = """React TypeScriptプロジェクトでのAPI統合のベストプラクティス：

## 1. 型安全なAPI設計
```typescript
interface ApiResponse<T> {
  data: T;
  status: number;
  message: string;
}

interface User {
  id: number;
  name: string;
  email: string;
}
```

## 2. Axiosベースのクライアント
```typescript
import axios from 'axios';

const apiClient = axios.create({
  baseURL: process.env.REACT_APP_API_URL,
  timeout: 10000,
});
```

## 3. React Queryの活用
```typescript
import { useQuery } from '@tanstack/react-query';

const useUsers = () => {
  return useQuery<User[]>({
    queryKey: ['users'],
    queryFn: () => apiClient.get<User[]>('/users').then(res => res.data)
  });
};
```

## 4. エラーハンドリング
```typescript
const ErrorBoundary = ({ children }) => {
  // エラーハンドリングロジック
};
```

このアプローチにより、型安全で保守性の高いAPI統合が実現できます。"""
    
    # ナレッジベースディレクトリ作成
    knowledge_dir = Path("knowledge_base/auto_generated")
    knowledge_dir.mkdir(parents=True, exist_ok=True)
    
    # タグ抽出テスト
    def extract_tags_from_question(question):
        tech_keywords = {
            'react': ['react', 'jsx', 'component'],
            'typescript': ['typescript', 'ts'],
            'api': ['api', 'rest', 'graphql', 'endpoint'],
            'frontend': ['frontend', 'ui', 'css', 'html'],
        }
        
        found_tags = []
        question_lower = question.lower()
        
        for category, keywords in tech_keywords.items():
            if any(keyword in question_lower for keyword in keywords):
                found_tags.append(category)
        
        return found_tags if found_tags else ['general']
    
    # ナレッジエントリ作成
    knowledge_entry = {
        "timestamp": datetime.now().isoformat(),
        "question": test_question['question'],
        "questioner": test_question['user'],
        "copilot_response": test_response,
        "auto_generated": True,
        "knowledge_type": "copilot-ai-response",
        "tags": extract_tags_from_question(test_question['question']),
        "test_mode": True
    }
    
    print(f"📋 抽出されたタグ: {knowledge_entry['tags']}")
    
    # JSON保存
    safe_filename = "test_react_typescript_api_integration"
    filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{safe_filename}.json"
    filepath = knowledge_dir / filename
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(knowledge_entry, f, ensure_ascii=False, indent=2)
    
    print(f"✅ テストナレッジ保存: {filepath}")
    
    # Markdownサマリー生成
    summary_file = knowledge_dir / "README.md"
    
    new_entry = f"""
## {knowledge_entry['timestamp'][:10]} - {knowledge_entry['question'][:100]}

**質問者**: {knowledge_entry['questioner']}  
**タグ**: {', '.join(knowledge_entry['tags'])}  
**生成日時**: {knowledge_entry['timestamp']}  
**テストモード**: {knowledge_entry['test_mode']}

### 質問
{knowledge_entry['question']}

### GitHub Copilot AI回答
{knowledge_entry['copilot_response'][:500]}...

---
"""
    
    # 既存の内容を読み込み
    existing_content = ""
    if summary_file.exists():
        with open(summary_file, 'r', encoding='utf-8') as f:
            existing_content = f.read()
    
    if not existing_content:
        content = f"""# AI自動開発パイプライン - 生成ナレッジベース

このディレクトリには、GitHub Copilot AIが自動生成したナレッジが蓄積されます。

## 📊 統計
- 生成開始日: {datetime.now().strftime('%Y-%m-%d')}
- 自動更新: 質問受信時
- 形式: JSON + Markdown

## 🧪 テストエントリ
{new_entry}

## 📋 ナレッジエントリ
"""
    else:
        content = existing_content + new_entry
    
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Markdownサマリー更新: {summary_file}")
    
    # 統計表示
    json_files = list(knowledge_dir.glob("*.json"))
    print(f"📊 現在のナレッジエントリ数: {len(json_files)}")
    
    # タグ別統計
    tag_stats = {}
    for json_file in json_files:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for tag in data.get('tags', []):
                    tag_stats[tag] = tag_stats.get(tag, 0) + 1
        except:
            continue
    
    print("🏷️ タグ別統計:")
    for tag, count in sorted(tag_stats.items()):
        print(f"  - {tag}: {count}件")
    
    print("\n✅ ナレッジ自動生成システムテスト完了")
    print("🎯 実際の質問が来た時に同様の処理が自動実行されます")
    
    return True

if __name__ == "__main__":
    test_knowledge_auto_generation()
