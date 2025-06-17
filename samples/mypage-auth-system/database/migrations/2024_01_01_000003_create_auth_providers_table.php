<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::create('auth_providers', function (Blueprint $table) {
            $table->id();
            $table->foreignId('user_id')->constrained()->onDelete('cascade');
            $table->enum('provider_type', [
                'line', 
                'firebase_email', 
                'firebase_google', 
                'firebase_twitter', 
                'trustdock'
            ])->comment('認証プロバイダー種別');
            $table->string('provider_id')->comment('プロバイダーユーザーID');
            $table->string('provider_email')->nullable()->comment('プロバイダーメール');
            $table->json('provider_data')->nullable()->comment('プロバイダー追加データ');
            $table->text('access_token')->nullable()->comment('アクセストークン');
            $table->text('refresh_token')->nullable()->comment('リフレッシュトークン');
            $table->timestamp('token_expires_at')->nullable()->comment('トークン有効期限');
            $table->boolean('is_primary')->default(false)->comment('メイン認証フラグ');
            $table->timestamps();
            
            $table->unique(['provider_type', 'provider_id']);
            $table->index(['user_id', 'provider_type']);
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('auth_providers');
    }
};
