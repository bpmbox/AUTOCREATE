<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Process;
use Illuminate\Support\Facades\Log;

class LaveloController extends Controller
{
    private $pythonPath;
    private $laveloPath;
    
    public function __construct()
    {
        $this->pythonPath = env('PYTHON_PATH', 'python3');
        $this->laveloPath = base_path('app/Http/Controllers/Gradio/gra_03_programfromdocs/lavelo.py');
    }
    
    /**
     * Lavelo AIシステムのメインページ表示
     */
    public function index()
    {
        return view('lavelo.index', [
            'title' => 'Lavelo AI - Laravel統合システム',
            'description' => 'AI×人間協働開発のためのプロンプト管理・システム生成・自動化システム',
            'gradio_url' => 'http://localhost:7860'
        ]);
    }
    
    /**
     * Lavelo AIシステムの起動
     */
    public function start(Request $request)
    {
        try {
            Log::info('Lavelo AI システム起動開始');
            
            // Pythonプロセスを起動
            $process = Process::start([
                $this->pythonPath,
                $this->laveloPath
            ]);
            
            // プロセスIDを保存（停止時に使用）
            session(['lavelo_pid' => $process->id()]);
            
            return response()->json([
                'status' => 'success',
                'message' => 'Lavelo AI システムを起動しました',
                'gradio_url' => 'http://localhost:7860',
                'pid' => $process->id()
            ]);
            
        } catch (\Exception $e) {
            Log::error('Lavelo AI システム起動エラー: ' . $e->getMessage());
            
            return response()->json([
                'status' => 'error',
                'message' => 'システム起動に失敗しました: ' . $e->getMessage()
            ], 500);
        }
    }
    
    /**
     * Lavelo AIシステムの停止
     */
    public function stop(Request $request)
    {
        try {
            $pid = session('lavelo_pid');
            
            if ($pid) {
                // プロセス終了
                Process::run(['kill', '-TERM', $pid]);
                session()->forget('lavelo_pid');
                
                Log::info('Lavelo AI システム停止: PID ' . $pid);
                
                return response()->json([
                    'status' => 'success', 
                    'message' => 'Lavelo AI システムを停止しました'
                ]);
            } else {
                return response()->json([
                    'status' => 'warning',
                    'message' => '実行中のプロセスが見つかりません'
                ]);
            }
            
        } catch (\Exception $e) {
            Log::error('Lavelo AI システム停止エラー: ' . $e->getMessage());
            
            return response()->json([
                'status' => 'error',
                'message' => 'システム停止に失敗しました: ' . $e->getMessage()
            ], 500);
        }
    }
    
    /**
     * システム状態確認
     */
    public function status()
    {
        try {
            $pid = session('lavelo_pid');
            $isRunning = false;
            
            if ($pid) {
                // プロセス存在確認
                $result = Process::run(['ps', '-p', $pid]);
                $isRunning = $result->successful();
            }
            
            return response()->json([
                'status' => 'success',
                'is_running' => $isRunning,
                'pid' => $pid,
                'gradio_url' => $isRunning ? 'http://localhost:7860' : null
            ]);
            
        } catch (\Exception $e) {
            return response()->json([
                'status' => 'error',
                'message' => $e->getMessage()
            ], 500);
        }
    }
    
    /**
     * システム実行（直接モード）
     */
    public function run(Request $request)
    {
        try {
            Log::info('Lavelo AI システム直接実行');
            
            $output = Process::run([
                $this->pythonPath,
                '-c',
                "
import sys
sys.path.append('" . dirname($this->laveloPath) . "')
from lavelo import run_lavelo_system
run_lavelo_system()
                "
            ]);
            
            return response()->json([
                'status' => 'success',
                'message' => 'システム実行完了',
                'output' => $output->output(),
                'gradio_url' => 'http://localhost:7860'
            ]);
            
        } catch (\Exception $e) {
            Log::error('Lavelo AI システム実行エラー: ' . $e->getMessage());
            
            return response()->json([
                'status' => 'error',
                'message' => 'システム実行に失敗しました: ' . $e->getMessage()
            ], 500);
        }
    }
}
