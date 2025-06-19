const axios = require('axios');
require('dotenv').config();

async function testGroqAPI() {
    const groqApiKey = process.env.GROQ_API_KEY;
    
    if (!groqApiKey) {
        console.error('❌ GROQ_API_KEY が環境変数に設定されていません');
        process.exit(1);
    }

    console.log('🔍 Groq API キーをテスト中...');
    
    try {
        const response = await axios.post('https://api.groq.com/openai/v1/chat/completions', {
            model: 'llama-3.1-70b-versatile',
            messages: [
                {
                    role: 'user',
                    content: 'こんにちは！簡単なテストメッセージです。'
                }
            ],
            max_tokens: 100,
            temperature: 0.7
        }, {
            headers: {
                'Authorization': `Bearer ${groqApiKey}`,
                'Content-Type': 'application/json'
            }
        });

        console.log('✅ Groq API テスト成功!');
        console.log('📤 送信メッセージ: こんにちは！簡単なテストメッセージです。');
        console.log('📥 受信レスポンス:', response.data.choices[0].message.content);
        console.log('🔢 使用トークン数:', response.data.usage.total_tokens);
        console.log('⚡ モデル:', response.data.model);
        
    } catch (error) {
        console.error('❌ Groq API テスト失敗:');
        
        if (error.response) {
            console.error('ステータス:', error.response.status);
            console.error('エラーメッセージ:', error.response.data);
        } else if (error.request) {
            console.error('リクエストエラー:', error.message);
        } else {
            console.error('その他のエラー:', error.message);
        }
        
        process.exit(1);
    }
}

// Groq API利用可能モデル一覧を取得
async function listGroqModels() {
    const groqApiKey = process.env.GROQ_API_KEY;
    
    if (!groqApiKey) {
        console.error('❌ GROQ_API_KEY が環境変数に設定されていません');
        return;
    }

    try {
        const response = await axios.get('https://api.groq.com/openai/v1/models', {
            headers: {
                'Authorization': `Bearer ${groqApiKey}`,
                'Content-Type': 'application/json'
            }
        });

        console.log('📋 利用可能なGroqモデル一覧:');
        response.data.data.forEach((model, index) => {
            console.log(`${index + 1}. ${model.id}`);
        });
        
    } catch (error) {
        console.error('❌ モデル一覧取得失敗:', error.response?.data || error.message);
    }
}

// コマンドライン引数に応じて実行
const command = process.argv[2];

switch (command) {
    case 'test':
        testGroqAPI();
        break;
    case 'models':
        listGroqModels();
        break;
    case 'both':
        (async () => {
            await testGroqAPI();
            console.log('\n' + '='.repeat(50) + '\n');
            await listGroqModels();
        })();
        break;
    default:
        console.log('使用方法:');
        console.log('  node groq_test.js test    - API接続テスト');
        console.log('  node groq_test.js models  - 利用可能モデル一覧');
        console.log('  node groq_test.js both    - 両方実行');
}
