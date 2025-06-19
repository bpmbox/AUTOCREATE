// 最も基本的な通知テスト（console.logで詳細追跡）
console.log('🚀 基本通知テストスクリプト読み込み開始');

function basicNotificationTest() {
    console.log('🧪 基本通知テスト開始');
    console.log('📋 Chrome notifications API確認:', !!chrome.notifications);
    console.log('📋 Chrome notifications create確認:', !!chrome.notifications.create);
    
    // 最も基本的なオプション
    const basicOptions = {
        type: 'basic',
        iconUrl: 'icon16.png',
        title: 'Basic Test',
        message: 'Basic test message'
    };
    
    console.log('📋 基本オプション作成完了:', basicOptions);
    console.log('📋 各プロパティ確認:');
    console.log('  - type:', basicOptions.type, '(type:', typeof basicOptions.type, ')');
    console.log('  - iconUrl:', basicOptions.iconUrl, '(type:', typeof basicOptions.iconUrl, ')');
    console.log('  - title:', basicOptions.title, '(type:', typeof basicOptions.title, ')');
    console.log('  - message:', basicOptions.message, '(type:', typeof basicOptions.message, ')');
    
    // JSON変換テスト
    try {
        const jsonString = JSON.stringify(basicOptions);
        console.log('📋 JSON変換成功:', jsonString);
        
        const parsedOptions = JSON.parse(jsonString);
        console.log('📋 JSON解析成功:', parsedOptions);
    } catch (jsonError) {
        console.error('❌ JSON処理エラー:', jsonError);
        return;
    }
    
    console.log('🚀 chrome.notifications.create実行開始...');
    
    try {
        chrome.notifications.create(basicOptions, function(notificationId) {
            console.log('📞 コールバック実行開始');
            console.log('📋 notificationId:', notificationId);
            console.log('📋 chrome.runtime.lastError:', chrome.runtime.lastError);
            
            if (chrome.runtime.lastError) {
                console.error('❌ 基本テスト失敗:');
                console.error('  - エラーメッセージ:', chrome.runtime.lastError.message);
                console.error('  - 使用オプション:', JSON.stringify(basicOptions, null, 2));
                
                // さらにシンプルなテスト
                console.log('🔄 さらにシンプルなテストを実行...');
                const simpleOptions = {
                    type: 'basic',
                    title: 'Simple',
                    message: 'Simple message'
                };
                
                chrome.notifications.create(simpleOptions, function(simpleId) {
                    if (chrome.runtime.lastError) {
                        console.error('❌ シンプルテストも失敗:', chrome.runtime.lastError.message);
                    } else {
                        console.log('✅ シンプルテスト成功:', simpleId);
                    }
                });
            } else {
                console.log('✅ 基本テスト成功:', notificationId);
                
                // 成功した場合は削除
                setTimeout(() => {
                    chrome.notifications.clear(notificationId, function(wasCleared) {
                        console.log('🗑️ 通知削除結果:', wasCleared);
                    });
                }, 3000);
            }
        });
    } catch (createError) {
        console.error('❌ chrome.notifications.create例外:', createError);
    }
}

// 拡張機能起動時に実行
chrome.runtime.onInstalled.addListener(() => {
    console.log('🔧 拡張機能インストール - 基本テスト実行');
    setTimeout(basicNotificationTest, 2000);
});

chrome.runtime.onStartup.addListener(() => {
    console.log('🔧 拡張機能起動 - 基本テスト実行');
    setTimeout(basicNotificationTest, 2000);
});

// メッセージリスナー
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.type === 'BASIC_NOTIFICATION_TEST') {
        console.log('📨 基本通知テストメッセージ受信');
        basicNotificationTest();
        sendResponse({success: true, message: '基本テスト実行'});
        return true;
    }
});

console.log('✅ 基本通知テストスクリプト読み込み完了');
