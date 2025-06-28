@echo off
REM 🎨 Laravel風 Artisan クイックコマンド (Windows)
REM 使用例: quick_commands.bat test

set PYTHON_EXEC=venv\Scripts\python.exe
set ARTISAN=%PYTHON_EXEC% artisan

if "%1"=="test" (
    echo 🧪 Copilot自動化システムテスト実行...
    %ARTISAN% test:copilot
    goto :end
)

if "%1"=="start" (
    echo 🚀 FastAPIサーバー起動...
    %ARTISAN% fastapi:start
    goto :end
)

if "%1"=="routes" (
    echo 🛣️ アクティブルート確認...
    %ARTISAN% route:active
    goto :end
)

if "%1"=="gradio" (
    echo 🎨 Gradio機能一覧...
    %ARTISAN% gradio:list
    goto :end
)

if "%1"=="cicd" (
    echo 🔄 完全CI/CDパイプライン実行...
    %ARTISAN% cicd full
    goto :end
)

if "%1"=="help" (
    echo.
    echo 🎨 Laravel風 Artisan クイックコマンド
    echo ================================
    echo quick_commands.bat test     - Copilotテスト
    echo quick_commands.bat start    - FastAPIサーバー起動
    echo quick_commands.bat routes   - アクティブルート確認
    echo quick_commands.bat gradio   - Gradio機能一覧
    echo quick_commands.bat cicd     - CI/CDパイプライン
    echo.
    echo 💡 フルコマンド例:
    echo %ARTISAN% make:controller UserController
    echo %ARTISAN% test:unit
    echo %ARTISAN% fastapi:integration
    goto :end
)

echo ❌ 不明なコマンド: %1
echo 💡 使用可能コマンド: test, start, routes, gradio, cicd, help

:end
