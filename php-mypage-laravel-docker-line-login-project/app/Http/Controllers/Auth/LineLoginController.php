<?php

namespace App\Http\Controllers\Auth;

use App\Http\Controllers\Controller;
use App\Models\User;
use App\Services\LineLoginService;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\Log;

class LineLoginController extends Controller
{
    protected $lineLoginService;

    public function __construct(LineLoginService $lineLoginService)
    {
        $this->lineLoginService = $lineLoginService;
    }

    /**
     * LINE ログインページへリダイレクト
     */
    public function redirect()
    {
        $state = str()->random(32);
        session(['line_login_state' => $state]);

        $lineLoginUrl = $this->lineLoginService->getAuthorizationUrl($state);
        
        return redirect($lineLoginUrl);
    }

    /**
     * LINE ログインコールバック処理
     */
    public function callback(Request $request)
    {
        try {
            // State検証（CSRF対策）
            $sessionState = session('line_login_state');
            $requestState = $request->get('state');

            if (!$sessionState || $sessionState !== $requestState) {
                Log::warning('LINE Login: Invalid state parameter');
                return redirect()->route('login')->with('error', 'ログインに失敗しました。');
            }

            // 認証コード取得
            $code = $request->get('code');
            if (!$code) {
                Log::warning('LINE Login: No authorization code received');
                return redirect()->route('login')->with('error', 'ログインがキャンセルされました。');
            }

            // アクセストークン取得
            $tokenData = $this->lineLoginService->getAccessToken($code);
            if (!$tokenData) {
                Log::error('LINE Login: Failed to get access token');
                return redirect()->route('login')->with('error', 'ログインに失敗しました。');
            }

            // ユーザープロフィール取得
            $lineProfile = $this->lineLoginService->getUserProfile($tokenData['access_token']);
            if (!$lineProfile) {
                Log::error('LINE Login: Failed to get user profile');
                return redirect()->route('login')->with('error', 'ユーザー情報の取得に失敗しました。');
            }

            // ユーザー情報をDBに保存または更新
            $user = $this->findOrCreateUser($lineProfile);

            // ログイン処理
            Auth::login($user, true);

            // ログイン時刻更新
            $user->update(['last_login_at' => now()]);

            Log::info('LINE Login successful', ['user_id' => $user->id]);

            return redirect()->intended('/mypage')->with('success', 'ログインしました！');

        } catch (\Exception $e) {
            Log::error('LINE Login error: ' . $e->getMessage(), ['trace' => $e->getTraceAsString()]);
            return redirect()->route('login')->with('error', 'ログイン処理中にエラーが発生しました。');
        } finally {
            // セッションのstateクリア
            session()->forget('line_login_state');
        }
    }

    /**
     * ユーザーを検索または新規作成
     */
    protected function findOrCreateUser($lineProfile)
    {
        $user = User::where('line_user_id', $lineProfile['userId'])->first();

        if ($user) {
            // 既存ユーザーの情報を更新
            $user->update([
                'name' => $lineProfile['displayName'],
                'avatar' => $lineProfile['pictureUrl'] ?? null,
                'line_profile_data' => $lineProfile,
            ]);
        } else {
            // 新規ユーザー作成
            $user = User::create([
                'line_user_id' => $lineProfile['userId'],
                'name' => $lineProfile['displayName'],
                'avatar' => $lineProfile['pictureUrl'] ?? null,
                'line_profile_data' => $lineProfile,
                'email_verified_at' => now(), // LINE認証済みとみなす
            ]);

            Log::info('New user created via LINE Login', ['user_id' => $user->id]);
        }

        return $user;
    }

    /**
     * ログアウト処理
     */
    public function logout(Request $request)
    {
        Auth::logout();

        $request->session()->invalidate();
        $request->session()->regenerateToken();

        return redirect('/')->with('success', 'ログアウトしました。');
    }
}
