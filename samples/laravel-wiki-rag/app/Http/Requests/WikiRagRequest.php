<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

/**
 * WIKI RAG検索リクエストバリデーション
 */
class WikiRagRequest extends FormRequest
{
    /**
     * Determine if the user is authorized to make this request.
     *
     * @return bool
     */
    public function authorize(): bool
    {
        return true; // 認証は必要に応じて実装
    }

    /**
     * Get the validation rules that apply to the request.
     *
     * @return array<string, mixed>
     */
    public function rules(): array
    {
        return [
            'query' => [
                'required',
                'string',
                'min:2',
                'max:500',
                'regex:/^[a-zA-Z0-9\s\p{Hiragana}\p{Katakana}\p{Han}ー〜！？、。（）「」【】・]+$/u'
            ],
            'max_results' => [
                'sometimes',
                'integer',
                'min:1',
                'max:100'
            ],
            'threshold' => [
                'sometimes',
                'numeric',
                'min:0',
                'max:1'
            ]
        ];
    }

    /**
     * Get the error messages for the defined validation rules.
     *
     * @return array<string, string>
     */
    public function messages(): array
    {
        return [
            'query.required' => '検索クエリは必須です。',
            'query.string' => '検索クエリは文字列である必要があります。',
            'query.min' => '検索クエリは2文字以上で入力してください。',
            'query.max' => '検索クエリは500文字以内で入力してください。',
            'query.regex' => '検索クエリには有効な文字のみ使用してください。',
            'max_results.integer' => '最大結果数は整数である必要があります。',
            'max_results.min' => '最大結果数は1以上である必要があります。',
            'max_results.max' => '最大結果数は100以下である必要があります。',
            'threshold.numeric' => '閾値は数値である必要があります。',
            'threshold.min' => '閾値は0以上である必要があります。',
            'threshold.max' => '閾値は1以下である必要があります。'
        ];
    }

    /**
     * Get custom attributes for validator errors.
     *
     * @return array<string, string>
     */
    public function attributes(): array
    {
        return [
            'query' => '検索クエリ',
            'max_results' => '最大結果数',
            'threshold' => '閾値'
        ];
    }

    /**
     * Handle a failed validation attempt.
     *
     * @param \Illuminate\Contracts\Validation\Validator $validator
     * @return void
     *
     * @throws \Illuminate\Validation\ValidationException
     */
    protected function failedValidation(\Illuminate\Contracts\Validation\Validator $validator)
    {
        if ($this->ajax()) {
            throw new \Illuminate\Validation\ValidationException($validator, response()->json([
                'success' => false,
                'errors' => $validator->errors()
            ], 422));
        }

        parent::failedValidation($validator);
    }
}
