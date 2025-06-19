// 接続テスト用スクリプト
console.log('🔗 接続テストスクリプト読み込み開始');

// 安全なメッセージ送信関数
function safeMessageSend(message, callback) {
    console.log('📤 安全メッセージ送信開始:', message);
    
    try {
        chrome.runtime.sendMessage(message, (response) => {
            if (chrome.runtime.lastError) {
                console.error('❌ メッセージ送信エラー:', chrome.runtime.lastError.message);
                if (callback) callback(null, chrome.runtime.lastError);
            } else {
                console.log('✅ メッセージ送信成功:', response);
                if (callback) callback(response, null);
            }
        });
    } catch (error) {
        console.error('❌ メッセージ送信例外:', error);
        if (callback) callback(null, error);
    }
}

// 接続テスト関数
function testExtensionConnection() {
    console.log('🧪 拡張機能接続テスト開始');
    
    // テスト1: GET_STATUS
    console.log('📋 テスト1: ステータス取得');
    safeMessageSend({type: 'GET_STATUS'}, (response, error) => {
        if (error) {
            console.error('❌ ステータス取得失敗:', error);
        } else {
            console.log('✅ ステータス取得成功:', response);
        }
    });
    
    // テスト2: BASIC_NOTIFICATION_TEST
    setTimeout(() => {
        console.log('📋 テスト2: 基本通知テスト');
        safeMessageSend({type: 'BASIC_NOTIFICATION_TEST'}, (response, error) => {
            if (error) {
                console.error('❌ 基本通知テスト失敗:', error);
            } else {
                console.log('✅ 基本通知テスト成功:', response);
            }
        });
    }, 2000);
    
    // テスト3: TEST_CONNECTION
    setTimeout(() => {
        console.log('📋 テスト3: 接続テスト');
        safeMessageSend({type: 'TEST_CONNECTION'}, (response, error) => {
            if (error) {
                console.error('❌ 接続テスト失敗:', error);
            } else {
                console.log('✅ 接続テスト成功:', response);
            }
        });
    }, 4000);
}

// 自動実行
setTimeout(testExtensionConnection, 3000);

// 手動実行用
window.testConnection = testExtensionConnection;
window.safeMessageSend = safeMessageSend;

console.log('✅ 接続テストスクリプト読み込み完了');
console.log('📋 手動実行: testConnection() または safeMessageSend({type: "GET_STATUS"})');
