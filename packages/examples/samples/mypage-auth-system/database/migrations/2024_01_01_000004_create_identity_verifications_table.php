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
        Schema::create('identity_verifications', function (Blueprint $table) {
            $table->id();
            $table->foreignId('user_id')->constrained()->onDelete('cascade');
            $table->enum('verification_type', [
                'basic', 
                'advanced', 
                'bank_account', 
                'address'
            ])->comment('認証種別');
            $table->enum('status', [
                'pending', 
                'processing', 
                'approved', 
                'rejected', 
                'expired'
            ])->default('pending')->comment('認証ステータス');
            $table->string('trustdock_user_id')->nullable()->comment('TrustDockユーザーID');
            $table->string('verification_id')->nullable()->comment('認証ID');
            $table->json('verification_data')->nullable()->comment('認証データ');
            $table->json('documents')->nullable()->comment('提出書類情報');
            $table->timestamp('verified_at')->nullable()->comment('認証完了日時');
            $table->timestamp('expires_at')->nullable()->comment('認証有効期限');
            $table->text('notes')->nullable()->comment('備考');
            $table->timestamps();
            
            $table->index(['user_id', 'verification_type']);
            $table->index(['status']);
            $table->index(['trustdock_user_id']);
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('identity_verifications');
    }
};
