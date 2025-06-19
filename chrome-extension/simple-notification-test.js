// シンプルな通知テスト関数
function simpleNotificationTest() {
    console.log('シンプル通知テスト開始');
    
    try {
        chrome.notifications.create({
            type: 'basic',
            title: 'テスト通知',
            message: 'これはシンプルなテスト通知です'
        }, (notificationId) => {
            if (chrome.runtime.lastError) {
                console.error('シンプル通知エラー:', chrome.runtime.lastError.message);
            } else {
                console.log('シンプル通知成功:', notificationId);
                
                // 3秒後に削除
                setTimeout(() => {
                    chrome.notifications.clear(notificationId);
                }, 3000);
            }
        });
    } catch (error) {
        console.error('シンプル通知例外:', error);
    }
}

// 拡張機能インストール時にテスト実行
chrome.runtime.onInstalled.addListener(() => {
    console.log('拡張機能インストール - 通知テスト実行');
    setTimeout(simpleNotificationTest, 2000);
});

// 手動テスト用関数
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.type === 'TEST_SIMPLE_NOTIFICATION') {
        simpleNotificationTest();
        sendResponse({success: true});
        return true;
    }
});
