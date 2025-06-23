<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * 🚀 Run the migrations.
     */
    public function up(): void
    {
        Schema::create('line_users', function (Blueprint $table) {
            $table->id();
            $table->string('line_user_id')->unique()->comment('LINE User ID');
            $table->string('display_name')->nullable()->comment('表示名');
            $table->string('picture_url')->nullable()->comment('プロフィール画像URL');
            $table->string('status_message')->nullable()->comment('ステータスメッセージ');
            $table->string('email')->nullable()->unique()->comment('メールアドレス');
            $table->timestamp('email_verified_at')->nullable();
            $table->string('language')->default('ja')->comment('言語設定');
            $table->json('line_profile')->nullable()->comment('LINEプロフィール情報(JSON)');
            $table->timestamp('last_login_at')->nullable()->comment('最終ログイン日時');
            $table->string('access_token')->nullable()->comment('アクセストークン');
            $table->string('refresh_token')->nullable()->comment('リフレッシュトークン');
            $table->timestamp('token_expires_at')->nullable()->comment('トークン有効期限');
            $table->boolean('is_active')->default(true)->comment('アカウント有効フラグ');
            $table->rememberToken();
            $table->timestamps();

            // 🔍 Indexes
            $table->index('line_user_id');
            $table->index('email');
            $table->index('last_login_at');
            $table->index('is_active');
        });
    }

    /**
     * 🔄 Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('line_users');
    }
};
