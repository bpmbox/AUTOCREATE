// テスト用の簡単な通知システム
function testNotification() {
    console.log('通知テスト開始');
    
    // 最もシンプルな通知
    try {
        chrome.notifications.create({
            type: 'basic',
            title: 'テスト通知',
            message: 'これはテスト用の通知です'
        }, (notificationId) => {
            if (chrome.runtime.lastError) {
                console.error('テスト通知エラー:', chrome.runtime.lastError.message);
            } else {
                console.log('テスト通知成功:', notificationId);
                
                // 3秒後に削除
                setTimeout(() => {
                    try {
                        chrome.notifications.clear(notificationId);
                        console.log('テスト通知削除完了');
                    } catch (clearError) {
                        console.error('テスト通知削除エラー:', clearError);
                    }
                }, 3000);
            }
        });
    } catch (error) {
        console.error('テスト通知作成エラー:', error);
    }
}

// 拡張機能起動時にテスト実行
chrome.runtime.onStartup.addListener(() => {
    setTimeout(testNotification, 1000);
});

chrome.runtime.onInstalled.addListener(() => {
    setTimeout(testNotification, 1000);
});
