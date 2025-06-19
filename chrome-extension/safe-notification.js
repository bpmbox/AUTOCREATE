// 通知プロパティ検証関数
function validateNotificationOptions(options) {
    const required = ['type', 'iconUrl', 'title', 'message'];
    const missing = [];
    
    for (const prop of required) {
        if (!options[prop]) {
            missing.push(prop);
        }
    }
    
    if (missing.length > 0) {
        console.error('❌ 必須プロパティが不足:', missing);
        return false;
    }
    
    console.log('✅ 通知プロパティ検証OK');
    return true;
}

// 安全な通知作成関数
function createSafeNotification(title, message, type = 'info') {
    // 引数の厳密な検証
    if (!title || typeof title !== 'string' || title.trim() === '') {
        title = 'AI President Monitor';
    }
    if (!message || typeof message !== 'string' || message.trim() === '') {
        message = 'Notification from AI President Monitor';
    }
    
    // 文字数制限
    title = title.substring(0, 100);
    message = message.substring(0, 300);
    
    // 通知オプション作成
    const options = {
        type: 'basic',
        iconUrl: 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDgiIGhlaWdodD0iNDgiIHZpZXdCb3g9IjAgMCA0OCA0OCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPGNpcmNsZSBjeD0iMjQiIGN5PSIyNCIgcj0iMjIiIGZpbGw9IiMwMDdBQ0MiLz4KPHN2ZyB4PSIxMiIgeT0iMTIiIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPgo8cGF0aCBkPSJNMTIgMkM2LjQ4IDIgMiA2LjQ4IDIgMTJTNi40OCAyMiAxMiAyMlMyMiAxNy41MiAyMiAxMlMxNy41MiAyIDEyIDJaTTEzIDEwVjE5SDExVjEwSDEzWk0xMSA2SDEzVjhIMTFWNloiIGZpbGw9IndoaXRlIi8+Cjwvc3ZnPgo8L3N2Zz4K',
        title: title,
        message: message
    };
    
    // プロパティ検証
    if (!validateNotificationOptions(options)) {
        console.error('❌ 通知オプション検証失敗');
        return false;
    }
    
    console.log('🚀 安全な通知作成開始:', options);
    
    try {
        chrome.notifications.create(options, (notificationId) => {
            if (chrome.runtime.lastError) {
                console.error('❌ 通知作成失敗:', chrome.runtime.lastError.message);
                console.error('🔍 失敗時のオプション:', JSON.stringify(options, null, 2));
            } else {
                console.log('✅ 通知作成成功:', notificationId);
                
                // 自動削除
                setTimeout(() => {
                    try {
                        chrome.notifications.clear(notificationId);
                        console.log('🗑️ 通知削除完了:', notificationId);
                    } catch (clearError) {
                        console.error('❌ 通知削除エラー:', clearError);
                    }
                }, 5000);
            }
        });
        return true;
    } catch (error) {
        console.error('❌ 通知作成例外:', error);
        return false;
    }
}

// テスト用関数
function testSafeNotification() {
    console.log('🧪 安全な通知テスト開始');
    
    const testCases = [
        { title: 'テスト1', message: '基本通知テスト' },
        { title: '', message: '空タイトルテスト' },
        { title: 'テスト3', message: '' },
        { title: null, message: null },
        { title: 'テスト5', message: '正常なテスト' }
    ];
    
    testCases.forEach((testCase, index) => {
        setTimeout(() => {
            console.log(`テストケース ${index + 1}:`, testCase);
            createSafeNotification(testCase.title, testCase.message);
        }, index * 2000);
    });
}

// メッセージリスナーに追加
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.type === 'TEST_SAFE_NOTIFICATION') {
        testSafeNotification();
        sendResponse({success: true});
        return true;
    }
    
    if (request.type === 'CREATE_SAFE_NOTIFICATION') {
        const result = createSafeNotification(request.title, request.message, request.type);
        sendResponse({success: result});
        return true;
    }
});
