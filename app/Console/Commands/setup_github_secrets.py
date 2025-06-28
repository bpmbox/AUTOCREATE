#!/usr/bin/env python3
"""
GitHub Secrets設定スクリプト
.envファイルから重要なAPIキーを読み取り、GitHub Secretsに設定するための手順を表示
"""

import os
import json
from pathlib import Path

def read_env_file():
    """環境変数ファイルを読み込み"""
    env_file = Path('.env')
    if not env_file.exists():
        print("❌ .envファイルが見つかりません")
        return {}
    
    env_vars = {}
    with open(env_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                env_vars[key] = value
    
    return env_vars

def generate_github_secrets_setup():
    """GitHub Secrets設定手順を生成"""
    env_vars = read_env_file()
    
    # 重要なAPIキー（GitHub Actionsで必要）
    important_secrets = {
        'HF_TOKEN': 'Hugging Face API Token',
        'GROQ_API_KEY': 'Groq API Key', 
        'OPENAI_API_KEY': 'OpenAI API Key',
        'SUPABASE_URL': 'Supabase Project URL',
        'SUPABASE_KEY': 'Supabase Anon Key',
        'GITHUB_TOKEN': 'GitHub Personal Access Token',
        'JIRA_API_TOKEN': 'JIRA API Token',
        'NOTION_TOKEN': 'Notion Integration Token',
        'MIIBO_API_KEY': 'miibo API Key'
    }
    
    print("🔐 GitHub Secrets設定ガイド")
    print("=" * 50)
    print("📝 以下のSecretsをGitHub リポジトリに設定してください:")
    print("🔗 https://github.com/bpmbox/AUTOCREATE/settings/secrets/actions")
    print()
    
    found_secrets = []
    
    for secret_name, description in important_secrets.items():
        if secret_name in env_vars and env_vars[secret_name]:
            value = env_vars[secret_name]
            if value != 'your_token_here' and value != 'hf_your_token_here':
                found_secrets.append({
                    'name': secret_name,
                    'value': value,
                    'description': description
                })
                print(f"✅ {secret_name}")
                print(f"   📝 Description: {description}")
                print(f"   🔑 Value: {value[:10]}...{value[-5:] if len(value) > 15 else value}")
                print()
    
    print("📋 設定手順:")
    print("1. GitHub Secrets ページを開く")
    print("2. 'New repository secret' をクリック")
    print("3. 上記のName/Valueを入力")
    print("4. 'Add secret' をクリック")
    print()
    print(f"📊 設定対象: {len(found_secrets)} 個のSecrets")
    
    # GitHub CLI使用の自動設定も提案
    print("\n🚀 GitHub CLI自動設定 (オプション):")
    print("以下のコマンドで一括設定可能:")
    print()
    
    for secret in found_secrets:
        # GitHub CLIコマンド生成（参考用）
        print(f"gh secret set {secret['name']} --body \"{secret['value']}\"")
    
    return found_secrets

if __name__ == "__main__":
    secrets = generate_github_secrets_setup()
    
    print("\n🎯 次のステップ:")
    print("1. GitHub Secretsを設定")
    print("2. GitHub Actions再実行")
    print("3. React+Vite+shadcn UI AIチャットアプリの公開確認")
    print("4. https://bpmbox.github.io/AUTOCREATE/chat/ でアクセス")
