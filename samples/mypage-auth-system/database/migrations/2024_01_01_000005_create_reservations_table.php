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
        Schema::create('reservations', function (Blueprint $table) {
            $table->id();
            $table->foreignId('user_id')->constrained()->onDelete('cascade');
            $table->string('reservation_number', 20)->unique()->comment('予約番号');
            $table->enum('service_type', [
                'consultation', 
                'support', 
                'maintenance', 
                'other'
            ])->comment('サービス種別');
            $table->timestamp('reserved_at')->comment('予約日時');
            $table->enum('status', [
                'pending', 
                'confirmed', 
                'completed', 
                'cancelled', 
                'no_show'
            ])->default('pending')->comment('予約ステータス');
            $table->json('reservation_data')->nullable()->comment('予約詳細');
            $table->decimal('amount', 10, 2)->unsigned()->nullable()->comment('金額');
            $table->text('notes')->nullable()->comment('備考');
            $table->timestamps();
            $table->timestamp('cancelled_at')->nullable()->comment('キャンセル日時');
            
            $table->index(['user_id', 'reserved_at']);
            $table->index(['status']);
            $table->index(['reservation_number']);
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('reservations');
    }
};
