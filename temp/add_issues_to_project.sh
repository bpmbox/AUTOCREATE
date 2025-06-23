#!/bin/bash

# AUTOCREATEプロジェクト管理スクリプト
# 全てのIssueをAUTOCREATEプロジェクト（#5）に追加

echo "🚀 AUTOCREATEプロジェクトにIssueを追加中..."

# Issue #36から#30まで追加
for i in {36..30}; do
    echo "📋 Issue #$i を追加中..."
    gh project item-add 5 --owner bpmbox --url https://github.com/bpmbox/AUTOCREATE/issues/$i
    sleep 1
done

# Issue #29から#25まで追加
for i in {29..25}; do
    echo "📋 Issue #$i を追加中..."
    gh project item-add 5 --owner bpmbox --url https://github.com/bpmbox/AUTOCREATE/issues/$i
    sleep 1
done

echo "✅ 完了！AUTOCREATEプロジェクトにIssueが追加されました"
echo "🔗 プロジェクトURL: https://github.com/orgs/bpmbox/projects/5"
