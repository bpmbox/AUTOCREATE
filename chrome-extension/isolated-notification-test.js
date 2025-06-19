// 完全に独立した通知テスト関数
function isolatedNotificationTest() {
    console.log('🧪 独立通知テスト開始');
    
    // ハードコードされた値で確実にテスト
    const hardcodedOptions = {
        type: 'basic',
        iconUrl: 'icon16.png',
        title: 'Test Notification',
        message: 'This is a test message'
    };
    
    console.log('📋 ハードコードオプション:', hardcodedOptions);
    
    // プロパティが存在するか再確認
    console.log('🔍 プロパティ確認:');
    console.log('- type:', hardcodedOptions.type, typeof hardcodedOptions.type);
    console.log('- iconUrl:', hardcodedOptions.iconUrl, typeof hardcodedOptions.iconUrl);
    console.log('- title:', hardcodedOptions.title, typeof hardcodedOptions.title);
    console.log('- message:', hardcodedOptions.message, typeof hardcodedOptions.message);
    
    try {
        chrome.notifications.create(hardcodedOptions, (notificationId) => {
            if (chrome.runtime.lastError) {
                console.error('❌ 独立テスト失敗:', chrome.runtime.lastError.message);
                console.error('❌ 使用したオプション:', JSON.stringify(hardcodedOptions, null, 2));
            } else {
                console.log('✅ 独立テスト成功:', notificationId);
                
                // 3秒後に削除
                setTimeout(() => {
                    chrome.notifications.clear(notificationId);
                    console.log('🗑️ 独立テスト通知削除完了');
                }, 3000);
            }
        });
    } catch (error) {
        console.error('❌ 独立テスト例外:', error);
    }
}

// 拡張機能がロードされた時に実行
setTimeout(() => {
    isolatedNotificationTest();
}, 3000);

// メッセージリスナーに追加
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.type === 'ISOLATED_NOTIFICATION_TEST') {
        isolatedNotificationTest();
        sendResponse({success: true});
        return true;
    }
});
