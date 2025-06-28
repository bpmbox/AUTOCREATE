<?php

namespace Tests\Unit;

use PHPUnit\Framework\TestCase;
use App\Models\LineUser;
use Illuminate\Foundation\Testing\RefreshDatabase;

class LineUserModelTest extends TestCase
{
    use RefreshDatabase;

    /**
     * 🧪 LINE ユーザーモデル作成テスト
     */
    public function test_can_create_line_user()
    {
        $userData = [
            'line_user_id' => 'test_line_user_123',
            'display_name' => 'テストユーザー',
            'picture_url' => 'https://example.com/avatar.jpg',
            'status_message' => 'テスト中です',
            'email' => 'test@example.com',
            'language' => 'ja',
            'is_active' => true,
        ];

        $user = LineUser::create($userData);

        $this->assertInstanceOf(LineUser::class, $user);
        $this->assertEquals('test_line_user_123', $user->line_user_id);
        $this->assertEquals('テストユーザー', $user->display_name);
        $this->assertTrue($user->is_active);
    }

    /**
     * 🔍 LINE ユーザー検索テスト
     */
    public function test_can_find_line_user_by_line_id()
    {
        $user = LineUser::create([
            'line_user_id' => 'search_test_123',
            'display_name' => '検索テストユーザー',
            'is_active' => true,
        ]);

        $foundUser = LineUser::where('line_user_id', 'search_test_123')->first();

        $this->assertInstanceOf(LineUser::class, $foundUser);
        $this->assertEquals('search_test_123', $foundUser->line_user_id);
        $this->assertEquals('検索テストユーザー', $foundUser->display_name);
    }

    /**
     * 🔄 LINE ユーザー更新テスト
     */
    public function test_can_update_line_user()
    {
        $user = LineUser::create([
            'line_user_id' => 'update_test_123',
            'display_name' => '更新前ユーザー',
            'is_active' => true,
        ]);

        $user->update([
            'display_name' => '更新後ユーザー',
            'status_message' => '更新されました',
        ]);

        $this->assertEquals('更新後ユーザー', $user->display_name);
        $this->assertEquals('更新されました', $user->status_message);
    }

    /**
     * 🚫 LINE ユーザー削除テスト
     */
    public function test_can_delete_line_user()
    {
        $user = LineUser::create([
            'line_user_id' => 'delete_test_123',
            'display_name' => '削除テストユーザー',
            'is_active' => true,
        ]);

        $userId = $user->id;
        $user->delete();

        $this->assertNull(LineUser::find($userId));
    }

    /**
     * 🔐 LINE ユーザー認証テスト
     */
    public function test_line_user_authentication_fields()
    {
        $user = LineUser::create([
            'line_user_id' => 'auth_test_123',
            'display_name' => '認証テストユーザー',
            'access_token' => 'test_access_token',
            'refresh_token' => 'test_refresh_token',
            'token_expires_at' => now()->addHours(1),
            'last_login_at' => now(),
            'is_active' => true,
        ]);

        $this->assertEquals('test_access_token', $user->access_token);
        $this->assertEquals('test_refresh_token', $user->refresh_token);
        $this->assertNotNull($user->token_expires_at);
        $this->assertNotNull($user->last_login_at);
    }

    /**
     * 📝 LINE プロフィール JSON テスト
     */
    public function test_line_profile_json_storage()
    {
        $profileData = [
            'userId' => 'profile_test_123',
            'displayName' => 'JSONテストユーザー',
            'pictureUrl' => 'https://example.com/profile.jpg',
            'statusMessage' => 'JSONテスト中'
        ];

        $user = LineUser::create([
            'line_user_id' => 'profile_test_123',
            'display_name' => 'JSONテストユーザー',
            'line_profile' => json_encode($profileData),
            'is_active' => true,
        ]);

        $decodedProfile = json_decode($user->line_profile, true);
        $this->assertEquals($profileData, $decodedProfile);
        $this->assertEquals('profile_test_123', $decodedProfile['userId']);
    }

    /**
     * ⚡ LINE ユーザー バリデーションテスト
     */
    public function test_line_user_validation()
    {
        $this->expectException(\Illuminate\Database\QueryException::class);

        // line_user_id が必須のため、空で作成するとエラー
        LineUser::create([
            'display_name' => 'バリデーションテスト',
            'is_active' => true,
        ]);
    }

    /**
     * 🎯 LINE ユーザー一意性テスト
     */
    public function test_line_user_id_uniqueness()
    {
        LineUser::create([
            'line_user_id' => 'unique_test_123',
            'display_name' => 'ユニークテスト1',
            'is_active' => true,
        ]);

        $this->expectException(\Illuminate\Database\QueryException::class);

        // 同じ line_user_id で作成するとエラー
        LineUser::create([
            'line_user_id' => 'unique_test_123',
            'display_name' => 'ユニークテスト2',
            'is_active' => true,
        ]);
    }
}
