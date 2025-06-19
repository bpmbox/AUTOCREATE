const { Client } = require('@notionhq/client');
require('dotenv').config();

const notion = new Client({ auth: process.env.NOTION_TOKEN });

// ナレッジベース作成用の関数群
async function createKnowledgeBase() {
    console.log('📚 AUTOCREATE ナレッジベース作成システム');
    console.log('=' * 50);
    
    const knowledgeItems = [
        {
            title: "🎯 AUTOCREATE システム概要",
            description: "AUTOCREATEプロジェクトの全体像とアーキテクチャ",
            category: "Overview",
            icon: "🎯",
            content: [
                "# AUTOCREATE システム概要",
                "",
                "## 🚀 主要機能",
                "- Notion API統合による知識管理自動化",
                "- Chrome拡張機能によるWeb自動化",
                "- XPath設定管理システム",
                "- AI-Human BPMSアシスタント",
                "",
                "## 🛠️ 技術スタック",
                "- **Backend**: Python, Node.js",
                "- **Frontend**: Chrome Extension, HTML/JS",
                "- **API**: Notion API, Supabase",
                "- **Automation**: XPath, DOM manipulation",
                "",
                "## 📊 システム構成",
                "```",
                "User Input → Chrome Extension → API Processing → Notion Knowledge Base",
                "```"
            ]
        },
        {
            title: "🔧 Notion API統合ガイド",
            description: "Notion APIの設定と使用方法の完全ガイド",
            category: "Integration",
            icon: "🔧",
            content: [
                "# Notion API統合ガイド",
                "",
                "## 🔑 API設定",
                "1. Notion開発者ページでインテグレーション作成",
                "2. Internal Integration Tokenを取得",
                "3. .envファイルに設定",
                "",
                "```bash",
                "NOTION_TOKEN=secret_your_token_here",
                "NOTION_DATABASE_ID=your_database_id",
                "```",
                "",
                "## 📄 ページ作成コマンド",
                "```bash",
                "make notion-sample      # サンプルページ",
                "make notion-autocreate  # AUTOCREATE知識",
                "make notion-technical   # 技術文書",
                "make notion-diagnostics # 診断実行",
                "```",
                "",
                "## 🎨 リッチコンテンツ機能",
                "- カバー画像自動設定",
                "- 絵文字アイコン",
                "- 構造化プロパティ",
                "- ネストしたブロック"
            ]
        },
        {
            title: "🌐 Chrome拡張機能活用法",
            description: "Chrome拡張機能とXPath設定による自動化テクニック",
            category: "Automation",
            icon: "🌐",
            content: [
                "# Chrome拡張機能活用法",
                "",
                "## 🎯 XPath設定管理",
                "```bash",
                "make chrome-ext-xpath-config  # 設定UI起動",
                "```",
                "",
                "## 📝 よく使うXPathパターン",
                "```javascript",
                "// チャット入力欄",
                "//textarea[@placeholder='メッセージを入力...']",
                "",
                "// 送信ボタン",
                "//button[contains(text(), '送信')]",
                "",
                "// フォーム要素",
                "//input[@name='message']",
                "//div[@contenteditable='true']",
                "```",
                "",
                "## 🔄 自動化ワークフロー",
                "1. Web要素を XPath で特定",
                "2. データ抽出・入力",
                "3. Notion API でナレッジ登録",
                "4. 結果確認・ログ出力"
            ]
        },
        {
            title: "🚀 Makefileコマンド一覧",
            description: "AUTOCREATE開発・運用で使える全コマンドリファレンス",
            category: "Reference",
            icon: "🚀",
            content: [
                "# Makefileコマンド一覧",
                "",
                "## 📋 Notion関連",
                "```bash",
                "make notion-demo           # デモモード",
                "make notion-test           # API接続テスト",
                "make notion-sample         # サンプルページ作成",
                "make notion-autocreate     # AUTOCREATE知識ページ",
                "make notion-technical      # 技術文書作成",
                "make notion-diagnostics    # 完全診断",
                "make notion-help           # ヘルプ表示",
                "```",
                "",
                "## 🌐 Chrome拡張機能",
                "```bash",
                "make chrome-ext            # 拡張機能起動",
                "make chrome-ext-test       # テストページ",
                "make chrome-ext-xpath-config # XPath設定",
                "make chrome-ext-status     # ステータス確認",
                "```",
                "",
                "## 🛠️ 開発・デバッグ",
                "```bash",
                "make app                   # アプリ起動",
                "make dev                   # 開発モード",
                "make debug                 # デバッグモード",
                "make gui                   # GUIデスクトップ",
                "```"
            ]
        },
        {
            title: "💡 よくある質問・トラブルシューティング",
            description: "開発中によく遭遇する問題と解決方法",
            category: "FAQ",
            icon: "💡",
            content: [
                "# よくある質問・トラブルシューティング",
                "",
                "## ❓ Notion API関連",
                "",
                "### Q: \"object_not_found\" エラーが出る",
                "**A**: データベースがインテグレーションと共有されていません",
                "1. Notionでデータベースを開く",
                "2. 「共有」→「インテグレーションを招待」",
                "3. n8nインテグレーションを選択",
                "",
                "### Q: \"validation_error\" が発生する",
                "**A**: プロパティ名が一致していません",
                "```bash",
                "make notion-diagnostics  # 実際のプロパティを確認",
                "```",
                "",
                "## 🌐 Chrome拡張機能関連",
                "",
                "### Q: XPathが動作しない",
                "**A**: ページ構造が変わった可能性があります",
                "1. 開発者ツールで要素を再確認",
                "2. XPath設定を更新",
                "3. テスト実行で確認",
                "",
                "### Q: 自動入力が失敗する",
                "**A**: タイミングの問題かもしれません",
                "- 待機時間を調整",
                "- 要素の読み込み完了を確認",
                "",
                "## 🔧 一般的な解決手順",
                "1. `make notion-diagnostics` で状態確認",
                "2. ログファイルでエラー詳細を確認",
                "3. 設定ファイル(.env)の内容確認",
                "4. 必要に応じて再設定・再起動"
            ]
        }
    ];
    
    console.log(`📚 ${knowledgeItems.length}個のナレッジアイテムを作成します...`);
    
    let successCount = 0;
    let results = [];
    
    for (const item of knowledgeItems) {
        try {
            console.log(`\n📝 作成中: ${item.title}`);
            
            const response = await notion.pages.create({
                "icon": {
                    "type": "emoji",
                    "emoji": item.icon
                },
                "parent": {
                    "type": "database_id",
                    "database_id": process.env.NOTION_DATABASE_ID
                },
                "properties": {
                    "Question 1": {
                        "title": [
                            {
                                "text": {
                                    "content": item.title
                                }
                            }
                        ]
                    },
                    "Question 2": {
                        "multi_select": [
                            {"name": item.category},
                            {"name": "Knowledge"},
                            {"name": "AUTOCREATE"}
                        ]
                    },
                    "Respondent": {
                        "rich_text": [
                            {
                                "text": {
                                    "content": item.description
                                }
                            }
                        ]
                    }
                },
                "children": item.content.map(line => {
                    if (line.startsWith('# ')) {
                        return {
                            "object": "block",
                            "type": "heading_1",
                            "heading_1": {
                                "rich_text": [{"text": {"content": line.substring(2)}}]
                            }
                        };
                    } else if (line.startsWith('## ')) {
                        return {
                            "object": "block",
                            "type": "heading_2",
                            "heading_2": {
                                "rich_text": [{"text": {"content": line.substring(3)}}]
                            }
                        };
                    } else if (line.startsWith('### ')) {
                        return {
                            "object": "block",
                            "type": "heading_3",
                            "heading_3": {
                                "rich_text": [{"text": {"content": line.substring(4)}}]
                            }
                        };
                    } else if (line.startsWith('```')) {
                        return {
                            "object": "block",
                            "type": "code",
                            "code": {
                                "rich_text": [{"text": {"content": line.replace(/```/g, '')}}],
                                "language": "javascript"
                            }
                        };
                    } else if (line.trim() === '') {
                        return {
                            "object": "block",
                            "type": "paragraph",
                            "paragraph": {
                                "rich_text": []
                            }
                        };
                    } else {
                        return {
                            "object": "block",
                            "type": "paragraph",
                            "paragraph": {
                                "rich_text": [{"text": {"content": line}}]
                            }
                        };
                    }
                })
            });
            
            console.log(`✅ 成功: ${item.title}`);
            console.log(`   Page ID: ${response.id}`);
            console.log(`   URL: ${response.url}`);
            
            results.push({
                title: item.title,
                id: response.id,
                url: response.url,
                status: 'success'
            });
            successCount++;
            
            // API制限を考慮して少し待機
            await new Promise(resolve => setTimeout(resolve, 1000));
            
        } catch (error) {
            console.log(`❌ 失敗: ${item.title}`);
            console.log(`   エラー: ${error.message}`);
            
            results.push({
                title: item.title,
                status: 'failed',
                error: error.message
            });
        }
    }
    
    console.log('\n' + '=' * 50);
    console.log('🎉 ナレッジベース作成完了！');
    console.log(`✅ 成功: ${successCount}/${knowledgeItems.length}`);
    console.log('\n📊 作成結果:');
    
    results.forEach(result => {
        if (result.status === 'success') {
            console.log(`✅ ${result.title}`);
            console.log(`   URL: ${result.url}`);
        } else {
            console.log(`❌ ${result.title} - ${result.error}`);
        }
    });
    
    return results;
}

// 実行
if (require.main === module) {
    createKnowledgeBase()
        .then(results => {
            const successCount = results.filter(r => r.status === 'success').length;
            console.log(`\n🚀 完了: ${successCount}個のナレッジページが作成されました！`);
        })
        .catch(error => {
            console.error('❌ エラーが発生しました:', error);
            process.exit(1);
        });
}

module.exports = { createKnowledgeBase };
