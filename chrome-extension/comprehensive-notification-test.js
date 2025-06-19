// 通知機能の包括的テスト
function comprehensiveNotificationTest() {
    console.log('🧪 包括的通知テスト開始');
    
    // テスト1: 基本通知
    setTimeout(() => {
        console.log('テスト1: 基本通知');
        chrome.notifications.create({
            type: 'basic',
            title: 'テスト1',
            message: '基本通知テスト'
        }, (id) => {
            if (chrome.runtime.lastError) {
                console.error('テスト1失敗:', chrome.runtime.lastError.message);
            } else {
                console.log('テスト1成功:', id);
            }
        });
    }, 1000);
    
    // テスト2: 長いメッセージ
    setTimeout(() => {
        console.log('テスト2: 長いメッセージ');
        chrome.notifications.create({
            type: 'basic',
            title: '長いタイトルのテストです。これは制限を超える可能性があります。',
            message: '非常に長いメッセージのテストです。この通知は文字数制限をテストするために作成されました。正常に表示されるかどうかを確認します。'
        }, (id) => {
            if (chrome.runtime.lastError) {
                console.error('テスト2失敗:', chrome.runtime.lastError.message);
            } else {
                console.log('テスト2成功:', id);
            }
        });
    }, 3000);
    
    // テスト3: 空の値
    setTimeout(() => {
        console.log('テスト3: 空の値');
        chrome.notifications.create({
            type: 'basic',
            title: '',
            message: ''
        }, (id) => {
            if (chrome.runtime.lastError) {
                console.error('テスト3失敗:', chrome.runtime.lastError.message);
            } else {
                console.log('テスト3成功:', id);
            }
        });
    }, 5000);
}

// 手動テスト用メッセージリスナー
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.type === 'RUN_COMPREHENSIVE_TEST') {
        comprehensiveNotificationTest();
        sendResponse({success: true, message: '包括的テスト開始'});
        return true;
    }
});
