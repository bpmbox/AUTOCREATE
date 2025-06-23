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
            $table->string('line_user_id')->unique()->index();
            $table->string('name');
            $table->string('email')->nullable()->unique();
            $table->string('avatar')->nullable();
            $table->json('line_profile_data')->nullable();
            $table->timestamp('email_verified_at')->nullable();
            $table->string('password')->nullable(); // LINE認証の場合不要
            $table->boolean('is_active')->default(true);
            $table->timestamp('last_login_at')->nullable();
            $table->string('remember_token')->nullable();
            $table->timestamps();
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
