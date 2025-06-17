<?php

namespace AutoCreate\MyPageAuth;

use Illuminate\Support\ServiceProvider as BaseServiceProvider;
use AutoCreate\MyPageAuth\Console\Commands\InstallCommand;
use AutoCreate\MyPageAuth\Console\Commands\PublishCommand;

class ServiceProvider extends BaseServiceProvider
{
    /**
     * Register any application services.
     */
    public function register(): void
    {
        // 設定ファイルをマージ
        $this->mergeConfigFrom(
            __DIR__.'/../config/mypage-auth.php',
            'mypage-auth'
        );

        // サービスを登録
        $this->app->singleton(\AutoCreate\MyPageAuth\Services\AuthService::class);
        $this->app->singleton(\AutoCreate\MyPageAuth\Services\TrustDockService::class);
        $this->app->singleton(\AutoCreate\MyPageAuth\Services\WikiRagService::class);
    }

    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        // マイグレーションを登録
        $this->loadMigrationsFrom(__DIR__.'/../database/migrations');

        // ルートを登録
        $this->loadRoutesFrom(__DIR__.'/../routes/web.php');
        $this->loadRoutesFrom(__DIR__.'/../routes/api.php');

        // ビューを登録
        $this->loadViewsFrom(__DIR__.'/../resources/views', 'mypage-auth');

        // 言語ファイルを登録
        $this->loadTranslationsFrom(__DIR__.'/../resources/lang', 'mypage-auth');

        // コマンドを登録
        if ($this->app->runningInConsole()) {
            $this->commands([
                InstallCommand::class,
                PublishCommand::class,
            ]);
        }

        // 公開可能なファイルを登録
        $this->publishes([
            __DIR__.'/../config/mypage-auth.php' => config_path('mypage-auth.php'),
        ], 'mypage-auth-config');

        $this->publishes([
            __DIR__.'/../database/migrations' => database_path('migrations'),
        ], 'mypage-auth-migrations');

        $this->publishes([
            __DIR__.'/../resources/views' => resource_path('views/vendor/mypage-auth'),
        ], 'mypage-auth-views');

        $this->publishes([
            __DIR__.'/../resources/js' => resource_path('js/vendor/mypage-auth'),
            __DIR__.'/../resources/css' => resource_path('css/vendor/mypage-auth'),
        ], 'mypage-auth-assets');

        $this->publishes([
            __DIR__.'/../resources/lang' => resource_path('lang/vendor/mypage-auth'),
        ], 'mypage-auth-lang');
    }
}
