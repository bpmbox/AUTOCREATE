#!/bin/bash
# AI応答システムの継続実行スクリプト

SCRIPT_DIR="/workspaces/AUTOCREATE"
PYTHON_SCRIPT="copilot_ai_responder_fixed.py"
PID_FILE="$SCRIPT_DIR/ai_responder.pid"
LOG_FILE="$SCRIPT_DIR/ai_responder_service.log"

start_ai_responder() {
    echo "🚀 AI応答システム開始中..." | tee -a "$LOG_FILE"
    cd "$SCRIPT_DIR"
    
    # 既存プロセスをチェック
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p "$PID" > /dev/null 2>&1; then
            echo "⚠️ AI応答システムは既に実行中です (PID: $PID)" | tee -a "$LOG_FILE"
            return 1
        else
            rm -f "$PID_FILE"
        fi
    fi
    
    # バックグラウンドで開始
    nohup python3 "$PYTHON_SCRIPT" >> "$LOG_FILE" 2>&1 &
    PID=$!
    echo $PID > "$PID_FILE"
    
    echo "✅ AI応答システム開始完了 (PID: $PID)" | tee -a "$LOG_FILE"
    echo "📋 ログ: $LOG_FILE"
    echo "🔗 チャット: http://localhost:8080"
}

stop_ai_responder() {
    echo "🛑 AI応答システム停止中..." | tee -a "$LOG_FILE"
    
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p "$PID" > /dev/null 2>&1; then
            kill "$PID"
            echo "✅ AI応答システム停止完了 (PID: $PID)" | tee -a "$LOG_FILE"
        else
            echo "⚠️ プロセスが見つかりません" | tee -a "$LOG_FILE"
        fi
        rm -f "$PID_FILE"
    else
        echo "⚠️ PIDファイルが見つかりません" | tee -a "$LOG_FILE"
    fi
    
    # 残存プロセスもクリーンアップ
    pkill -f "copilot_ai_responder_fixed.py"
}

status_ai_responder() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p "$PID" > /dev/null 2>&1; then
            echo "✅ AI応答システム実行中 (PID: $PID)"
            echo "📊 プロセス情報:"
            ps -p "$PID" -o pid,ppid,cmd,etime,pcpu,pmem
            echo "📋 最新ログ (最後の5行):"
            tail -5 "$LOG_FILE"
        else
            echo "❌ AI応答システム停止中 (PIDファイルは存在)"
            rm -f "$PID_FILE"
        fi
    else
        echo "❌ AI応答システム停止中"
    fi
}

case "$1" in
    start)
        start_ai_responder
        ;;
    stop)
        stop_ai_responder
        ;;
    status)
        status_ai_responder
        ;;
    restart)
        stop_ai_responder
        sleep 2
        start_ai_responder
        ;;
    *)
        echo "使用法: $0 {start|stop|status|restart}"
        echo ""
        echo "  start   - AI応答システムを開始"
        echo "  stop    - AI応答システムを停止" 
        echo "  status  - AI応答システムの状態確認"
        echo "  restart - AI応答システムを再起動"
        exit 1
        ;;
esac
