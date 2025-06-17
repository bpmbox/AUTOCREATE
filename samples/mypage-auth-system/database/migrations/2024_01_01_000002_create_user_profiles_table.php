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
        Schema::create('user_profiles', function (Blueprint $table) {
            $table->id();
            $table->foreignId('user_id')->constrained()->onDelete('cascade');
            $table->string('first_name', 50)->nullable()->comment('姓');
            $table->string('last_name', 50)->nullable()->comment('名');
            $table->string('first_name_kana', 50)->nullable()->comment('姓（カナ）');
            $table->string('last_name_kana', 50)->nullable()->comment('名（カナ）');
            $table->date('birth_date')->nullable()->comment('生年月日');
            $table->enum('gender', ['male', 'female', 'other', 'prefer_not_to_say'])->nullable()->comment('性別');
            $table->string('postal_code', 10)->nullable()->comment('郵便番号');
            $table->text('address')->nullable()->comment('住所');
            $table->string('avatar_url', 500)->nullable()->comment('アバター画像URL');
            $table->json('preferences')->nullable()->comment('設定情報');
            $table->timestamps();
            
            $table->unique(['user_id']);
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('user_profiles');
    }
};
