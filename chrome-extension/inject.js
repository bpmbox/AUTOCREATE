/**
 * AUTOCREATE AI社長 - ページ注入スクリプト
 * Web APIアクセス用
 */

console.log('🤖 AI社長注入スクリプト読み込み');

// ページレベルでのSupabase監視
window.aiPresidentInject = {
    supabaseConfig: {
        url: 'https://rootomzbucovwdqsscqd.supabase.co',
        key: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJvb3RvbXpidWNvdndkcXNzY3FkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzU4OTE4ODMsImV4cCI6MjA1MTQ2Nzg4M30.fYKOe-HPh4WUdvBhEJxakLWCMQBp4E90EDwARk7ucf8'
    },
    
    // リアルタイム監視
    async startRealtimeMonitoring() {
        try {
            // WebSocketまたはServer-Sent Events
            const eventSource = new EventSource(`${this.supabaseConfig.url}/rest/v1/chat_history`);
            
            eventSource.onmessage = (event) => {
                const data = JSON.parse(event.data);
                console.log('📡 リアルタイムメッセージ:', data);
                
                // コンテンツスクリプトに通知
                window.postMessage({
                    type: 'AI_PRESIDENT_REALTIME_MESSAGE',
                    data: data
                }, '*');
            };
            
        } catch (error) {
            console.error('❌ リアルタイム監視エラー:', error);
        }
    },
    
    // 直接Supabaseアクセス
    async fetchLatestMessages() {
        try {
            const response = await fetch(`${this.supabaseConfig.url}/rest/v1/chat_history?select=*&order=created.desc&limit=10`, {
                headers: {
                    'apikey': this.supabaseConfig.key,
                    'Authorization': `Bearer ${this.supabaseConfig.key}`
                }
            });
            
            return await response.json();
            
        } catch (error) {
            console.error('❌ メッセージ取得エラー:', error);
            return [];
        }
    }
};

// ページ読み込み完了時に開始
if (document.readyState === 'complete') {
    window.aiPresidentInject.startRealtimeMonitoring();
} else {
    window.addEventListener('load', () => {
        window.aiPresidentInject.startRealtimeMonitoring();
    });
}

// メッセージリスナー
window.addEventListener('message', (event) => {
    if (event.data.type === 'AI_PRESIDENT_REALTIME_MESSAGE') {
        console.log('📬 リアルタイムメッセージ受信:', event.data);
    }
});
