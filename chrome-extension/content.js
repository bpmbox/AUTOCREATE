/**
 * AUTOCREATE AI社長 - コンテンツスクリプト
 * ページ内の入力欄を自動操作
 */

console.log('🤖 AI社長コンテンツスクリプト読み込み完了');

let aiPresidentMonitor = {
    active: false,
    inputSelector: null,
    submitSelector: null,
    currentSite: null
};

// ページの種類を判定して適切なセレクターを設定
function detectPageType() {
    const url = window.location.href;
    
    if (url.includes('processmaker.com')) {
        aiPresidentMonitor.currentSite = 'processmaker';
        // ProcessMaker用のセレクター（実際のサイト構造に合わせて調整が必要）
        aiPresidentMonitor.inputSelector = 'input[type="text"], textarea, [contenteditable="true"]';
        aiPresidentMonitor.submitSelector = 'button[type="submit"], .btn-primary, .submit-btn';
        
    } else if (url.includes('skyoffice.me')) {
        aiPresidentMonitor.currentSite = 'skyoffice';
        // SkyOffice用のセレクター
        aiPresidentMonitor.inputSelector = '.chat-input, .message-input, input[placeholder*="message"], textarea[placeholder*="message"]';
        aiPresidentMonitor.submitSelector = '.send-btn, .chat-send, button[type="submit"]';
        
    } else if (url.includes('supabase.co')) {
        aiPresidentMonitor.currentSite = 'supabase';
        // Supabase Dashboard用
        aiPresidentMonitor.inputSelector = 'input, textarea';
        aiPresidentMonitor.submitSelector = 'button';
        
    } else {
        // 汎用的なチャット・入力欄検出
        aiPresidentMonitor.currentSite = 'generic';
        aiPresidentMonitor.inputSelector = 'input[type="text"], textarea, [contenteditable="true"], .chat-input, .message-input';
        aiPresidentMonitor.submitSelector = 'button[type="submit"], .send-btn, .submit-btn';
    }
    
    console.log(`🎯 サイト検出: ${aiPresidentMonitor.currentSite}`);
    console.log(`📝 入力欄セレクター: ${aiPresidentMonitor.inputSelector}`);
    console.log(`🚀 送信ボタンセレクター: ${aiPresidentMonitor.submitSelector}`);
}

// 入力欄を検出
function findInputField() {
    const inputs = document.querySelectorAll(aiPresidentMonitor.inputSelector);
    
    // 表示されている入力欄を優先して選択
    for (const input of inputs) {
        if (input.offsetWidth > 0 && input.offsetHeight > 0 && !input.disabled) {
            return input;
        }
    }
    
    return inputs[0] || null;
}

// 送信ボタンを検出
function findSubmitButton() {
    const buttons = document.querySelectorAll(aiPresidentMonitor.submitSelector);
    
    for (const button of buttons) {
        if (button.offsetWidth > 0 && button.offsetHeight > 0 && !button.disabled) {
            return button;
        }
    }
    
    return buttons[0] || null;
}

// メッセージを入力欄に自動入力
function autoInputMessage(message) {
    const inputField = findInputField();
    
    if (!inputField) {
        console.warn('⚠️ 入力欄が見つかりません');
        showNotification('入力欄が見つかりません', 'warning');
        return false;
    }
    
    try {
        // 入力欄にフォーカス
        inputField.focus();
        
        // 値を設定
        if (inputField.contentEditable === 'true') {
            // contenteditable要素の場合
            inputField.textContent = message;
            inputField.innerHTML = message;
        } else {
            // input/textarea要素の場合
            inputField.value = message;
        }
        
        // 入力イベントを発火
        const inputEvent = new Event('input', { bubbles: true });
        inputField.dispatchEvent(inputEvent);
        
        const changeEvent = new Event('change', { bubbles: true });
        inputField.dispatchEvent(changeEvent);
        
        console.log('✅ メッセージ入力完了:', message.substring(0, 50) + '...');
        
        // 送信ボタンを自動クリック（オプション）
        setTimeout(() => {
            autoSubmitMessage();
        }, 1000);
        
        return true;
        
    } catch (error) {
        console.error('❌ 自動入力エラー:', error);
        showNotification('自動入力エラー', 'error');
        return false;
    }
}

// メッセージを自動送信
function autoSubmitMessage() {
    const submitButton = findSubmitButton();
    
    if (!submitButton) {
        console.warn('⚠️ 送信ボタンが見つかりません');
        showNotification('送信ボタンが見つかりません', 'warning');
        return false;
    }
    
    try {
        // 送信ボタンをクリック
        submitButton.click();
        
        console.log('✅ メッセージ送信完了');
        showNotification('AI社長応答送信完了', 'success');
        
        return true;
        
    } catch (error) {
        console.error('❌ 自動送信エラー:', error);
        showNotification('自動送信エラー', 'error');
        return false;
    }
}

// 通知表示
function showNotification(message, type = 'info') {
    // 既存の通知があれば削除
    const existingNotification = document.querySelector('.ai-president-notification');
    if (existingNotification) {
        existingNotification.remove();
    }
    
    // 通知要素作成
    const notification = document.createElement('div');
    notification.className = `ai-president-notification ai-president-${type}`;
    notification.textContent = `🤖 AI社長: ${message}`;
    
    // スタイル設定
    Object.assign(notification.style, {
        position: 'fixed',
        top: '20px',
        right: '20px',
        padding: '12px 16px',
        backgroundColor: type === 'success' ? '#4CAF50' : type === 'warning' ? '#FF9800' : type === 'error' ? '#F44336' : '#2196F3',
        color: 'white',
        borderRadius: '4px',
        boxShadow: '0 2px 8px rgba(0,0,0,0.2)',
        zIndex: '10000',
        fontSize: '14px',
        maxWidth: '300px',
        transition: 'all 0.3s ease'
    });
    
    document.body.appendChild(notification);
    
    // 3秒後に自動削除
    setTimeout(() => {
        notification.style.opacity = '0';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }, 3000);
}

// メッセージリスナー
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    console.log('📨 メッセージ受信:', request);
    
    if (request.type === 'INIT_AI_PRESIDENT_MONITOR') {
        detectPageType();
        aiPresidentMonitor.active = true;
        showNotification('AI社長監視システム起動', 'success');
        sendResponse({ success: true, site: aiPresidentMonitor.currentSite });
    }
    
    if (request.type === 'AUTO_INPUT_MESSAGE') {
        const success = autoInputMessage(request.message);
        sendResponse({ success });
        
        // 元メッセージの情報も表示
        if (request.originalMessage) {
            console.log('📬 元メッセージ:', request.originalMessage);
        }
    }
    
    if (request.type === 'MANUAL_INPUT') {
        const success = autoInputMessage(request.message);
        sendResponse({ success });
    }
    
    if (request.type === 'GET_PAGE_INFO') {
        sendResponse({
            site: aiPresidentMonitor.currentSite,
            inputFound: !!findInputField(),
            submitFound: !!findSubmitButton(),
            active: aiPresidentMonitor.active
        });
    }
});

// ページ読み込み完了時の初期化
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        setTimeout(detectPageType, 1000);
    });
} else {
    setTimeout(detectPageType, 1000);
}

// DOM変更監視（動的コンテンツ対応）
const observer = new MutationObserver((mutations) => {
    let shouldRedetect = false;
    
    mutations.forEach((mutation) => {
        if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
            // 新しい要素が追加された場合、入力欄があるかチェック
            for (const node of mutation.addedNodes) {
                if (node.nodeType === Node.ELEMENT_NODE) {
                    if (node.matches && (node.matches('input') || node.matches('textarea') || node.matches('[contenteditable]'))) {
                        shouldRedetect = true;
                        break;
                    }
                }
            }
        }
    });
    
    if (shouldRedetect) {
        setTimeout(detectPageType, 500);
    }
});

observer.observe(document.body, {
    childList: true,
    subtree: true
});

console.log('🎯 AI社長コンテンツスクリプト初期化完了');
