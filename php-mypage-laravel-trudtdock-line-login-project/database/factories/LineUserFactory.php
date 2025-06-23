<?php

namespace Database\Factories;

use App\Models\LineUser;
use Illuminate\Database\Eloquent\Factories\Factory;

/**
 * 🧪 LINE ユーザーファクトリー
 * テスト用のダミーデータ生成
 */
class LineUserFactory extends Factory
{
    /**
     * The name of the factory's corresponding model.
     *
     * @var string
     */
    protected $model = LineUser::class;

    /**
     * Define the model's default state.
     *
     * @return array<string, mixed>
     */
    public function definition(): array
    {
        return [
            'line_user_id' => 'test_' . $this->faker->unique()->numberBetween(100000, 999999),
            'display_name' => $this->faker->name(),
            'picture_url' => $this->faker->imageUrl(300, 300, 'people'),
            'status_message' => $this->faker->optional()->sentence(),
            'email' => $this->faker->optional()->unique()->safeEmail(),
            'language' => $this->faker->randomElement(['ja', 'en', 'ko', 'zh']),
            'line_profile' => json_encode([
                'userId' => 'test_' . $this->faker->unique()->numberBetween(100000, 999999),
                'displayName' => $this->faker->name(),
                'pictureUrl' => $this->faker->imageUrl(300, 300, 'people'),
                'statusMessage' => $this->faker->optional()->sentence(),
            ]),
            'last_login_at' => $this->faker->optional()->dateTimeBetween('-1 month', 'now'),
            'access_token' => $this->faker->optional()->sha256(),
            'refresh_token' => $this->faker->optional()->sha256(),
            'token_expires_at' => $this->faker->optional()->dateTimeBetween('now', '+1 hour'),
            'is_active' => $this->faker->boolean(90), // 90%の確率でアクティブ
        ];
    }

    /**
     * 🔐 アクティブユーザー状態
     */
    public function active(): static
    {
        return $this->state(fn (array $attributes) => [
            'is_active' => true,
            'last_login_at' => now(),
        ]);
    }

    /**
     * 🚫 非アクティブユーザー状態
     */
    public function inactive(): static
    {
        return $this->state(fn (array $attributes) => [
            'is_active' => false,
            'last_login_at' => $this->faker->dateTimeBetween('-6 months', '-1 month'),
        ]);
    }

    /**
     * 📧 メール確認済み状態
     */
    public function emailVerified(): static
    {
        return $this->state(fn (array $attributes) => [
            'email' => $this->faker->unique()->safeEmail(),
            'email_verified_at' => now(),
        ]);
    }

    /**
     * 🎯 特定のLINE IDを指定
     */
    public function withLineId(string $lineId): static
    {
        return $this->state(fn (array $attributes) => [
            'line_user_id' => $lineId,
        ]);
    }

    /**
     * 👤 特定の名前を指定
     */
    public function withName(string $name): static
    {
        return $this->state(fn (array $attributes) => [
            'display_name' => $name,
        ]);
    }

    /**
     * 🔑 認証トークン付き
     */
    public function withTokens(): static
    {
        return $this->state(fn (array $attributes) => [
            'access_token' => 'test_access_token_' . $this->faker->unique()->sha256(),
            'refresh_token' => 'test_refresh_token_' . $this->faker->unique()->sha256(),
            'token_expires_at' => now()->addHours(1),
        ]);
    }

    /**
     * 🇯🇵 日本語ユーザー
     */
    public function japanese(): static
    {
        return $this->state(fn (array $attributes) => [
            'language' => 'ja',
            'display_name' => $this->faker->name('ja_JP'),
        ]);
    }

    /**
     * 🌐 英語ユーザー
     */
    public function english(): static
    {
        return $this->state(fn (array $attributes) => [
            'language' => 'en',
            'display_name' => $this->faker->name('en_US'),
        ]);
    }
}
