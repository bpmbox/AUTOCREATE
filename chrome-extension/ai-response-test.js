// AI大統領応答機能テスト
// Test AI President Response Function

console.log('🧪 AI大統領応答機能テストを開始します...');
console.log('🧪 Starting AI President Response Function Test...');

// テストデータセット - 様々なエッジケース
const testCases = [
    // 正常なケース
    { description: '正常なメッセージ', data: { message: 'こんにちは', username: 'テストユーザー' } },
    { description: 'Normal message', data: { message: 'Hello', username: 'TestUser' } },
    
    // undefinedケース
    { description: 'undefined メッセージ', data: { message: undefined, username: 'テストユーザー' } },
    { description: 'undefined message', data: { message: undefined, username: 'TestUser' } },
    
    // nullケース
    { description: 'null メッセージ', data: { message: null, username: 'テストユーザー' } },
    { description: 'null message', data: { message: null, username: 'TestUser' } },
    
    // 空文字列ケース
    { description: '空文字列メッセージ', data: { message: '', username: 'テストユーザー' } },
    { description: 'empty string message', data: { message: '', username: 'TestUser' } },
    
    // オブジェクト全体がundefined
    { description: 'メッセージオブジェクト全体がundefined', data: undefined },
    { description: 'entire message object undefined', data: undefined },
    
    // 空オブジェクト
    { description: '空オブジェクト', data: {} },
    { description: 'empty object', data: {} },
    
    // 特殊な文字
    { description: '特殊文字を含むメッセージ', data: { message: '質問？ありがとう！', username: '特殊ユーザー' } },
    { description: 'special characters message', data: { message: 'Question? Thank you!', username: 'SpecialUser' } },
    
    // 非文字列型
    { description: '数値メッセージ', data: { message: 12345, username: 'NumberUser' } },
    { description: 'number message', data: { message: 12345, username: 'NumberUser' } },
    
    // 配列メッセージ
    { description: '配列メッセージ', data: { message: ['配列', 'メッセージ'], username: 'ArrayUser' } },
    { description: 'array message', data: { message: ['array', 'message'], username: 'ArrayUser' } }
];

// バックグラウンドスクリプトにテストメッセージを送信
async function runTests() {
    console.log(`📊 ${testCases.length}個のテストケースを実行中...`);
    console.log(`📊 Running ${testCases.length} test cases...`);
    
    for (let i = 0; i < testCases.length; i++) {
        const testCase = testCases[i];
        console.log(`\n🧪 テスト ${i + 1}/${testCases.length}: ${testCase.description}`);
        console.log(`🧪 Test ${i + 1}/${testCases.length}: ${testCase.description}`);
        
        try {
            // バックグラウンドスクリプトにテストメッセージを送信
            const response = await new Promise((resolve, reject) => {
                chrome.runtime.sendMessage({
                    type: 'test_ai_response',
                    data: testCase.data
                }, (response) => {
                    if (chrome.runtime.lastError) {
                        reject(chrome.runtime.lastError);
                    } else {
                        resolve(response);
                    }
                });
            });
            
            console.log('✅ テスト成功:', response);
            console.log('✅ Test success:', response);
            
        } catch (error) {
            console.error('❌ テスト失敗:', error);
            console.error('❌ Test failed:', error);
        }
        
        // 次のテストまで少し待機
        await new Promise(resolve => setTimeout(resolve, 100));
    }
    
    console.log('\n🎉 すべてのテストが完了しました！');
    console.log('🎉 All tests completed!');
}

// テスト実行
runTests().catch(error => {
    console.error('❌ テスト実行中にエラーが発生しました:', error);
    console.error('❌ Error occurred during test execution:', error);
});
