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
        Schema::create('users', function (Blueprint $table) {
            $table->id();
            $table->uuid('uuid')->unique()->comment('UUID');
            $table->string('email')->unique()->comment('メールアドレス');
            $table->string('name')->comment('表示名');
            $table->string('phone', 20)->nullable()->comment('電話番号');
            $table->timestamp('email_verified_at')->nullable()->comment('メール認証日時');
            $table->timestamps();
            $table->softDeletes();
            
            $table->index(['email']);
            $table->index(['uuid']);
            $table->index(['deleted_at']);
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('users');
    }
};
