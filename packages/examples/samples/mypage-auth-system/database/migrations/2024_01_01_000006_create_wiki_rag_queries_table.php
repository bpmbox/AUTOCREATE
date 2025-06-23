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
        Schema::create('wiki_rag_queries', function (Blueprint $table) {
            $table->id();
            $table->foreignId('user_id')->constrained()->onDelete('cascade');
            $table->text('query')->comment('クエリ内容');
            $table->json('results')->nullable()->comment('検索結果');
            $table->decimal('response_time', 8, 3)->unsigned()->nullable()->comment('応答時間（秒）');
            $table->integer('result_count')->unsigned()->nullable()->comment('結果件数');
            $table->string('session_id')->nullable()->comment('セッションID');
            $table->timestamp('created_at')->useCurrent();
            
            $table->index(['user_id', 'created_at']);
            $table->index(['session_id']);
            $table->fullText(['query']);
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('wiki_rag_queries');
    }
};
