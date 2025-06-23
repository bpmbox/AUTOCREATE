<?php

namespace Tests\Feature;

use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class LineLoginTest extends TestCase
{
    use RefreshDatabase;

    /**
     * 🔐 LINE Login開始テスト
     */
    public function test_line_login_redirect()
    {
        $response = $this->get('/auth/line');
        
        $response->assertStatus(302);
        $response->assertRedirect();
        
        // リダイレクト先がLINE認証URLかチェック
        $location = $response->headers->get('Location');
        $this->assertStringContainsString('access.line.me', $location);
        $this->assertStringContainsString('oauth2', $location);
    }

    /**
     * 🏚️ ログインページ表示テスト
     */
    public function test_login_page_display()
    {
        $response = $this->get('/login');
        
        $response->assertStatus(200);
        $response->assertSee('LINE ログイン');
        $response->assertSee('LINEでログイン');
    }

    /**
     * 🔒 認証が必要なページのテスト
     */
    public function test_mypage_requires_authentication()
    {
        $response = $this->get('/mypage');
        
        // 認証なしでアクセスすると認証ページにリダイレクト
        $response->assertStatus(302);
    }

    /**
     * 🌐 API エンドポイントテスト
     */
    public function test_api_user_endpoint_requires_auth()
    {
        $response = $this->get('/api/user');
        
        $response->assertStatus(302); // 認証なしは302リダイレクト
    }

    /**
     * 🏠 ホームページテスト
     */
    public function test_home_page_shows_login()
    {
        $response = $this->get('/');
        
        $response->assertStatus(200);
        $response->assertSee('LINE ログイン');
    }
}
