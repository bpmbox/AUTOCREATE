<?php

namespace App\Http\Controllers\Auth;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Log;
use App\Models\LineUser;

class LineLoginController extends Controller
{
    /**
     * 🚀 LINE Login開始
     */
    public function redirectToLine()
    {
        $channelId = config('services.line.channel_id');
        $callbackUrl = config('services.line.callback_url');
        $state = csrf_token();
        
        // 📝 SESSION に state 保存
        session(['line_login_state' => $state]);
        
        $params = [
            'response_type' => 'code',
            'client_id' => $channelId,
            'redirect_uri' => $callbackUrl,
            'state' => $state,
            'scope' => 'profile openid email',
        ];
        
        $lineAuthUrl = 'https://access.line.me/oauth2/v2.1/authorize?' . http_build_query($params);
        
        Log::info('🔐 LINE Login開始', ['url' => $lineAuthUrl]);
        
        return redirect($lineAuthUrl);
    }
    
    /**
     * 🔄 LINE Loginコールバック処理
     */
    public function handleLineCallback(Request $request)
    {
        try {
            // 🔒 State検証
            $state = $request->get('state');
            $sessionState = session('line_login_state');
            
            if (!$state || $state !== $sessionState) {
                Log::error('❌ LINE Login State不一致', [
                    'request_state' => $state,
                    'session_state' => $sessionState
                ]);
                return redirect('/login')->with('error', 'セキュリティエラーが発生しました。');
            }
            
            $code = $request->get('code');
            if (!$code) {
                Log::error('❌ LINE Login認証コード取得失敗');
                return redirect('/login')->with('error', 'LINE認証に失敗しました。');
            }
            
            // 🎫 アクセストークン取得
            $tokenResponse = $this->getAccessToken($code);
            if (!$tokenResponse) {
                return redirect('/login')->with('error', 'トークン取得に失敗しました。');
            }
            
            // 👤 ユーザープロフィール取得
            $userProfile = $this->getUserProfile($tokenResponse['access_token']);
            if (!$userProfile) {
                return redirect('/login')->with('error', 'プロフィール取得に失敗しました。');
            }
            
            // 📝 ユーザー登録/更新
            $user = $this->createOrUpdateUser($userProfile, $tokenResponse);
            
            // 🔐 ログイン処理
            Auth::guard('line')->login($user);
            
            Log::info('✅ LINE Login成功', ['user_id' => $user->id]);
            
            return redirect('/mypage')->with('success', 'ログインしました！');
            
        } catch (\Exception $e) {
            Log::error('💥 LINE Loginエラー', [
                'error' => $e->getMessage(),
                'trace' => $e->getTraceAsString()
            ]);
            
            return redirect('/login')->with('error', 'ログイン処理中にエラーが発生しました。');
        }
    }
    
    /**
     * 🎫 アクセストークン取得
     */
    private function getAccessToken($code)
    {
        try {
            $response = Http::asForm()->post('https://api.line.me/oauth2/v2.1/token', [
                'grant_type' => 'authorization_code',
                'code' => $code,
                'redirect_uri' => config('services.line.callback_url'),
                'client_id' => config('services.line.channel_id'),
                'client_secret' => config('services.line.channel_secret'),
            ]);
            
            if ($response->successful()) {
                return $response->json();
            }
            
            Log::error('❌ アクセストークン取得失敗', [
                'status' => $response->status(),
                'body' => $response->body()
            ]);
            
            return null;
            
        } catch (\Exception $e) {
            Log::error('💥 アクセストークン取得エラー', ['error' => $e->getMessage()]);
            return null;
        }
    }
    
    /**
     * 👤 ユーザープロフィール取得
     */
    private function getUserProfile($accessToken)
    {
        try {
            $response = Http::withHeaders([
                'Authorization' => 'Bearer ' . $accessToken
            ])->get('https://api.line.me/v2/profile');
            
            if ($response->successful()) {
                return $response->json();
            }
            
            Log::error('❌ プロフィール取得失敗', [
                'status' => $response->status(),
                'body' => $response->body()
            ]);
            
            return null;
            
        } catch (\Exception $e) {
            Log::error('💥 プロフィール取得エラー', ['error' => $e->getMessage()]);
            return null;
        }
    }
    
    /**
     * 📝 ユーザー登録/更新
     */
    private function createOrUpdateUser($profile, $tokenData)
    {
        $user = LineUser::updateOrCreate(
            ['line_user_id' => $profile['userId']],
            [
                'display_name' => $profile['displayName'],
                'picture_url' => $profile['pictureUrl'] ?? null,
                'status_message' => $profile['statusMessage'] ?? null,
                'line_profile' => json_encode($profile),
                'access_token' => $tokenData['access_token'],
                'refresh_token' => $tokenData['refresh_token'] ?? null,
                'token_expires_at' => now()->addSeconds($tokenData['expires_in']),
                'last_login_at' => now(),
                'is_active' => true,
            ]
        );
        
        Log::info('👤 ユーザー情報更新', ['user_id' => $user->id]);
        
        return $user;
    }
    
    /**
     * 🚪 ログアウト
     */
    public function logout(Request $request)
    {
        Auth::guard('line')->logout();
        $request->session()->invalidate();
        $request->session()->regenerateToken();
        
        Log::info('👋 ログアウト完了');
        
        return redirect('/')->with('success', 'ログアウトしました。');
    }
}
