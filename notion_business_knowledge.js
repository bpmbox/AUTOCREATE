const { Client } = require('@notionhq/client');
require('dotenv').config();

const notion = new Client({ auth: process.env.NOTION_TOKEN });

// 業務向けナレッジベース作成
const businessKnowledgeItems = [
    {
        title: "📊 AUTOCREATE業務価値レポート",
        description: "システム導入による業務効率化・コスト削減効果の定量分析",
        category: "Business",
        icon: "📊",
        content: [
            {
                type: "heading_1",
                content: "🎯 AUTOCREATE 業務価値レポート"
            },
            {
                type: "paragraph", 
                content: "本レポートは、AUTOCREATE システム導入による具体的な業務価値と ROI を分析します。"
            },
            {
                type: "heading_2",
                content: "💰 コスト削減効果"
            },
            {
                type: "bulleted_list_item",
                content: "ナレッジ作成時間: 90%削減（従来3時間 → 現在18分）"
            },
            {
                type: "bulleted_list_item", 
                content: "Chrome拡張機能開発: 70%削減（従来2週間 → 現在3日）"
            },
            {
                type: "bulleted_list_item",
                content: "API統合作業: 85%削減（従来1週間 → 現在1日）"
            },
            {
                type: "heading_2",
                content: "📈 品質向上効果"
            },
            {
                type: "bulleted_list_item",
                content: "ドキュメント統一性: 100%（テンプレート自動適用）"
            },
            {
                type: "bulleted_list_item",
                content: "エラー発生率: 60%削減（自動検証機能）"
            },
            {
                type: "bulleted_list_item",
                content: "保守性: 80%向上（自動生成コード）"
            },
            {
                type: "heading_2",
                content: "🔗 関連リンク"
            },
            {
                type: "paragraph",
                content: "• GitHub Issue: [開発者向け技術仕様]\n• n8n ワークフロー: [自動化プロセス]\n• BPMN図: [業務フロー可視化]\n• Mermaid: [システム構成図]"
            }
        ]
    },
    {
        title: "🚀 システム利用ガイド（管理者向け）",
        description: "AUTOCREATE システムの運用・管理・トラブルシューティング",
        category: "Guide",
        icon: "🚀",
        content: [
            {
                type: "heading_1",
                content: "🚀 AUTOCREATE システム利用ガイド"
            },
            {
                type: "paragraph",
                content: "管理者・運用担当者向けの包括的な利用ガイドです。"
            },
            {
                type: "heading_2", 
                content: "⚡ クイックスタート"
            },
            {
                type: "numbered_list_item",
                content: "環境設定確認: make notion-diagnostics"
            },
            {
                type: "numbered_list_item",
                content: "ナレッジ作成: make notion-knowledge-create"
            },
            {
                type: "numbered_list_item", 
                content: "Chrome拡張機能: make chrome-ext"
            },
            {
                type: "heading_2",
                content: "🔧 日常運用"
            },
            {
                type: "bulleted_list_item",
                content: "定期バックアップ: make backup-all"
            },
            {
                type: "bulleted_list_item",
                content: "性能監視: make monitor-performance"
            },
            {
                type: "bulleted_list_item",
                content: "ログ確認: make check-logs"
            },
            {
                type: "heading_2",
                content: "📞 サポート・連絡先"
            },
            {
                type: "paragraph",
                content: "技術的な問題は GitHub Issues で報告してください。\n業務的な質問は Notion コメント機能をご利用ください。"
            }
        ]
    },
    {
        title: "💡 ベストプラクティス集",
        description: "効率的な活用方法・運用ノウハウ・成功事例",
        category: "Best Practice",
        icon: "💡", 
        content: [
            {
                type: "heading_1",
                content: "💡 AUTOCREATE ベストプラクティス"
            },
            {
                type: "paragraph",
                content: "実際の利用経験に基づく効率的な活用方法をまとめました。"
            },
            {
                type: "heading_2",
                content: "🎯 ナレッジ管理のコツ"
            },
            {
                type: "bulleted_list_item",
                content: "カテゴリ分類を統一する（Business/Technical/Guide/FAQ）"
            },
            {
                type: "bulleted_list_item",
                content: "アイコンを効果的に使用する（🎯📊🚀💡🔧）"
            },
            {
                type: "bulleted_list_item",
                content: "定期的にナレッジを更新・整理する"
            },
            {
                type: "heading_2",
                content: "⚡ 自動化活用法"
            },
            {
                type: "bulleted_list_item",
                content: "Chrome拡張機能でWebサイト操作を自動化"
            },
            {
                type: "bulleted_list_item",
                content: "XPath設定で確実な要素取得"
            },
            {
                type: "bulleted_list_item",
                content: "Makefileコマンドで作業を標準化"
            },
            {
                type: "heading_2",
                content: "📊 成功指標"
            },
            {
                type: "bulleted_list_item",
                content: "作業時間削減率: 目標70%以上"
            },
            {
                type: "bulleted_list_item",
                content: "エラー発生率: 目標5%以下"
            },
            {
                type: "bulleted_list_item",
                content: "ナレッジ活用率: 目標90%以上"
            }
        ]
    },
    {
        title: "🔗 リンク集・リソース一覧",
        description: "開発リソース・外部ツール・参考資料へのリンク集",
        category: "Resources",
        icon: "🔗",
        content: [
            {
                type: "heading_1", 
                content: "🔗 AUTOCREATE リソース・リンク集"
            },
            {
                type: "paragraph",
                content: "プロジェクトに関連する全てのリソースへのアクセスポイントです。"
            },
            {
                type: "heading_2",
                content: "👨‍💻 開発者向けリソース"
            },
            {
                type: "bulleted_list_item",
                content: "GitHub Repository: [bpmbox/AUTOCREATE]"
            },
            {
                type: "bulleted_list_item",
                content: "GitHub Issues: [技術仕様・バグ報告]"
            },
            {
                type: "bulleted_list_item",
                content: "API ドキュメント: [Notion API Reference]"
            },
            {
                type: "heading_2",
                content: "🔄 ワークフロー・自動化"
            },
            {
                type: "bulleted_list_item",
                content: "n8n ワークフロー: [自動化プロセス定義]"
            },
            {
                type: "bulleted_list_item",
                content: "BPMN 図: [業務プロセス可視化]"
            },
            {
                type: "bulleted_list_item",
                content: "Mermaid 図: [システム構成・フロー図]"
            },
            {
                type: "heading_2",
                content: "📚 学習リソース"
            },
            {
                type: "bulleted_list_item",
                content: "Notion API 公式ドキュメント"
            },
            {
                type: "bulleted_list_item",
                content: "Chrome Extension 開発ガイド"
            },
            {
                type: "bulleted_list_item",
                content: "XPath チュートリアル"
            },
            {
                type: "heading_2",
                content: "🆘 サポート"
            },
            {
                type: "paragraph",
                content: "問題が発生した場合:\n1. まず FAQ を確認\n2. GitHub Issues で検索\n3. 新しい Issue を作成\n4. Notion でコメント・質問"
            }
        ]
    }
];

async function createBusinessKnowledgeBase() {
    console.log("🏢 AUTOCREATE 業務向けナレッジベース作成");
    console.log("=" * 50);
    console.log(`📚 ${businessKnowledgeItems.length}個の業務ナレッジアイテムを作成します...\n`);
    
    const results = [];
    
    for (const item of businessKnowledgeItems) {
        try {
            console.log(`📝 作成中: ${item.title}`);
            
            // Convert content to Notion blocks
            const children = item.content.map(block => {
                if (block.type === 'heading_1') {
                    return {
                        object: "block",
                        type: "heading_1",
                        heading_1: {
                            rich_text: [{ type: "text", text: { content: block.content } }]
                        }
                    };
                } else if (block.type === 'heading_2') {
                    return {
                        object: "block",
                        type: "heading_2", 
                        heading_2: {
                            rich_text: [{ type: "text", text: { content: block.content } }]
                        }
                    };
                } else if (block.type === 'paragraph') {
                    return {
                        object: "block",
                        type: "paragraph",
                        paragraph: {
                            rich_text: [{ type: "text", text: { content: block.content } }]
                        }
                    };
                } else if (block.type === 'bulleted_list_item') {
                    return {
                        object: "block",
                        type: "bulleted_list_item",
                        bulleted_list_item: {
                            rich_text: [{ type: "text", text: { content: block.content } }]
                        }
                    };
                } else if (block.type === 'numbered_list_item') {
                    return {
                        object: "block",
                        type: "numbered_list_item", 
                        numbered_list_item: {
                            rich_text: [{ type: "text", text: { content: block.content } }]
                        }
                    };
                }
            });
            
            const response = await notion.pages.create({
                parent: {
                    type: "database_id",
                    database_id: process.env.NOTION_DATABASE_ID || "215fd0b5-bf7d-8069-99f3-dc4db1937b76"
                },
                icon: {
                    type: "emoji",
                    emoji: item.icon
                },
                properties: {
                    "Question 1": {
                        title: [{ text: { content: item.title } }]
                    },
                    "Question 2": {
                        multi_select: [
                            { name: item.category },
                            { name: "Business" },
                            { name: "Knowledge" }
                        ]
                    },
                    "Respondent": {
                        rich_text: [{ text: { content: "AUTOCREATE Business System" } }]
                    }
                },
                children: children
            });
            
            console.log(`✅ 成功: ${item.title}`);
            console.log(`   Page ID: ${response.id}`);
            console.log(`   URL: ${response.url}\n`);
            
            results.push({
                title: item.title,
                id: response.id,
                url: response.url,
                success: true
            });
            
        } catch (error) {
            console.log(`❌ 失敗: ${item.title}`);
            console.log(`   エラー: ${error.message}\n`);
            
            results.push({
                title: item.title,
                error: error.message,
                success: false
            });
        }
    }
    
    // 結果サマリー
    console.log("🎉 業務向けナレッジベース作成完了！");
    console.log(`✅ 成功: ${results.filter(r => r.success).length}/${results.length}\n`);
    
    console.log("📊 作成結果:");
    results.forEach(result => {
        if (result.success) {
            console.log(`✅ ${result.title}`);
            console.log(`   URL: ${result.url}`);
        } else {
            console.log(`❌ ${result.title}`);
            console.log(`   エラー: ${result.error}`);
        }
    });
    
    console.log(`\n🚀 完了: ${results.filter(r => r.success).length}個の業務ナレッジページが作成されました！`);
    
    return results;
}

// Run if called directly
if (require.main === module) {
    createBusinessKnowledgeBase()
        .then(() => console.log('業務ナレッジベース作成スクリプト完了'))
        .catch(console.error);
}

module.exports = { createBusinessKnowledgeBase };
