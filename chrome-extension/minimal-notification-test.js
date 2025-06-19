// 最小限の通知テスト
function minimalNotificationTest() {
    console.log('🧪 最小限通知テスト開始');
    
    // 最も基本的な通知（アイコンなし）
    const options = {
        type: 'basic',
        title: 'AI President Monitor',
        message: 'テスト通知です'
    };
    
    console.log('📋 最小限オプション:', options);
    
    chrome.notifications.create(options, (notificationId) => {
        if (chrome.runtime.lastError) {
            console.error('❌ 最小限通知エラー:', chrome.runtime.lastError.message);
            
            // さらにシンプルにしたテスト
            console.log('🔄 さらにシンプルなテストを実行...');
            chrome.notifications.create({
                type: 'basic',
                title: 'Test',
                message: 'Simple test'
            }, (id) => {
                if (chrome.runtime.lastError) {
                    console.error('❌ シンプルテストも失敗:', chrome.runtime.lastError.message);
                } else {
                    console.log('✅ シンプルテスト成功:', id);
                }
            });
        } else {
            console.log('✅ 最小限通知成功:', notificationId);
            
            // 成功した場合は3秒後に削除
            setTimeout(() => {
                chrome.notifications.clear(notificationId);
                console.log('🗑️ 通知削除完了');
            }, 3000);
        }
    });
}

// 通知権限の確認
function checkNotificationPermissions() {
    console.log('🔍 通知権限チェック開始');
    
    if (chrome.permissions) {
        chrome.permissions.contains({
            permissions: ['notifications']
        }, (result) => {
            console.log('📋 通知権限状態:', result);
            if (!result) {
                console.warn('⚠️ 通知権限が許可されていません');
            }
        });
    }
}

// 拡張機能起動時に実行
chrome.runtime.onStartup.addListener(() => {
    checkNotificationPermissions();
    setTimeout(minimalNotificationTest, 2000);
});

chrome.runtime.onInstalled.addListener(() => {
    checkNotificationPermissions();
    setTimeout(minimalNotificationTest, 2000);
});

// メッセージリスナー
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.type === 'TEST_MINIMAL_NOTIFICATION') {
        minimalNotificationTest();
        sendResponse({success: true});
        return true;
    }
    
    if (request.type === 'CHECK_PERMISSIONS') {
        checkNotificationPermissions();
        sendResponse({success: true});
        return true;
    }
});
