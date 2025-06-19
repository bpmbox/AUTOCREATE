// 包括的TypeError修正テスト
// Comprehensive TypeError Fix Test

console.log('🧪 包括的TypeError修正テストを開始します...');

// テストケース - 実際のSupabaseからの様々な応答パターンをシミュレート
const testMessages = [
    // 正常なケース
    {
        id: 1,
        ownerid: 'testuser',
        messages: 'こんにちは、AI社長！',
        created: '2025-06-17T10:00:00Z'
    },
    
    // owneridがundefined
    {
        id: 2,
        ownerid: undefined,
        messages: 'owneridがundefinedです',
        created: '2025-06-17T10:01:00Z'
    },
    
    // messagesがundefined
    {
        id: 3,
        ownerid: 'testuser2',
        messages: undefined,
        created: '2025-06-17T10:02:00Z'
    },
    
    // 両方ともundefined
    {
        id: 4,
        ownerid: undefined,
        messages: undefined,
        created: '2025-06-17T10:03:00Z'
    },
    
    // 完全に空のオブジェクト
    {
        id: 5
    },
    
    // null値
    {
        id: 6,
        ownerid: null,
        messages: null,
        created: '2025-06-17T10:04:00Z'
    },
    
    // 異なるプロパティ名
    {
        id: 7,
        username: 'alternative_user',
        content: '異なるプロパティ名です',
        created: '2025-06-17T10:05:00Z'
    },
    
    // AI社長メッセージ（フィルタリングされるべき）
    {
        id: 8,
        ownerid: 'AI社長',
        messages: 'これはAI社長のメッセージです',
        created: '2025-06-17T10:06:00Z'
    }
];

// メッセージフィルタリングのテスト
function testMessageFiltering() {
    console.log('\n🔍 メッセージフィルタリングテスト開始');
    
    const processedMessages = new Set(); // 空のセット
    
    try {
        // background.jsのフィルタリングロジックをシミュレート
        const newUserMessages = testMessages.filter(msg => {
            // メッセージIDとowneridの安全な確認
            if (!msg || !msg.id) {
                console.warn('⚠️ 無効なメッセージオブジェクト:', msg);
                return false;
            }
            
            // 既に処理済みかチェック
            if (processedMessages.has(msg.id)) {
                return false;
            }
            
            // owneridの安全なチェック
            const ownerId = msg.ownerid || msg.owner || msg.username || msg.user || '';
            const systemUsers = ['AI社長', 'ai-assistant', 'system'];
            
            return !systemUsers.includes(ownerId);
        });
        
        console.log('✅ フィルタリング成功');
        console.log(`📊 フィルタリング結果: ${newUserMessages.length}/${testMessages.length}件が処理対象`);
        
        // 各メッセージの詳細ログ
        newUserMessages.forEach((msg, index) => {
            const ownerId = msg.ownerid || msg.username || '不明';
            console.log(`  ${index + 1}. ID:${msg.id}, Owner:${ownerId}`);
        });
        
        return { success: true, filteredMessages: newUserMessages };
        
    } catch (error) {
        console.error('❌ フィルタリングエラー:', error);
        return { success: false, error: error.message };
    }
}

// メッセージ処理のテスト
async function testMessageProcessing() {
    console.log('\n🔍 メッセージ処理テスト開始');
    
    const testResult = testMessageFiltering();
    if (!testResult.success) {
        console.error('❌ フィルタリングが失敗したため、処理テストをスキップ');
        return;
    }
    
    const messagesToProcess = testResult.filteredMessages;
    let successCount = 0;
    let failCount = 0;
    
    for (const message of messagesToProcess) {
        try {
            console.log(`\n📝 メッセージ処理テスト: ID ${message.id}`);
            
            // processNewMessage関数のロジックをシミュレート
            const safeMessage = message || {};
            const ownerId = safeMessage.ownerid || safeMessage.owner || safeMessage.username || safeMessage.user || '不明なユーザー';
            const messageContent = safeMessage.messages || safeMessage.message || safeMessage.content || '空のメッセージ';
            
            console.log(`  📋 安全なデータ抽出: Owner=${ownerId}, Content=${messageContent.toString().substring(0, 30)}...`);
            
            // AI応答生成のテスト
            const response = await new Promise((resolve, reject) => {
                chrome.runtime.sendMessage({
                    type: 'test_ai_response',
                    data: safeMessage
                }, (response) => {
                    if (chrome.runtime.lastError) {
                        reject(chrome.runtime.lastError);
                    } else {
                        resolve(response);
                    }
                });
            });
            
            if (response.success) {
                console.log(`  ✅ AI応答生成成功: ${response.response.substring(0, 50)}...`);
                successCount++;
            } else {
                console.log(`  ❌ AI応答生成失敗: ${response.error}`);
                failCount++;
            }
            
        } catch (error) {
            console.error(`  ❌ メッセージ処理例外: ${error.message}`);
            failCount++;
        }
    }
    
    console.log(`\n📊 メッセージ処理結果: 成功=${successCount}, 失敗=${failCount}`);
    
    if (failCount === 0) {
        console.log('🎉 すべてのメッセージ処理が成功しました！');
    } else {
        console.log(`⚠️ ${failCount}件の処理で問題が発生しました`);
    }
}

// テスト実行
async function runComprehensiveTest() {
    console.log('🚀 包括的テスト実行開始');
    
    // Chrome拡張機能の存在確認
    if (!chrome.runtime) {
        console.error('❌ Chrome拡張機能が読み込まれていません');
        return;
    }
    
    console.log('✅ Chrome拡張機能確認完了');
    
    // フィルタリングテスト
    testMessageFiltering();
    
    // メッセージ処理テスト
    await testMessageProcessing();
    
    console.log('\n🏁 包括的テスト完了');
}

// テスト実行
runComprehensiveTest().catch(error => {
    console.error('❌ テスト実行エラー:', error);
});
