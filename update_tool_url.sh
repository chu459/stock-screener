#!/bin/bash
# 更新增长任务中的工具链接
# 使用方法: ./update_tool_url.sh <公共URL>

set -e

if [ -z "$1" ]; then
    echo "❌ 请提供公共URL作为参数"
    echo "用法: $0 <公共URL>"
    echo "示例: $0 https://smart-stock-screener.onrender.com"
    exit 1
fi

NEW_URL="$1"
echo "🔗 更新工具链接为: $NEW_URL"

# 创建临时目录
TEMP_DIR=".cowork-temp"
mkdir -p "$TEMP_DIR"

# 创建更新JSON
UPDATE_JSON="$TEMP_DIR/update_growth_new.json"
cat > "$UPDATE_JSON" << EOF
{
  "prompt": "你是一个在股市摸爬滚打15年的老股民，说话直接，不废话，观点犀利。在雪球/知乎/股吧参与讨论时，你以精准的判断和毒舌的点评著称。\n\n执行步骤：\n1. 扫描最新问题，选择1个有代表性的\n2. 生成高质量回答（150-300字）：\n   - 先一针见血指出问题本质（不超过2句话）\n   - 给出3条具体、可操作的强硬建议（用命令式语气，避免\"可能\"\"也许\"）\n   - 用简单直白的语言，可以适当使用口语化表达\n   - 最后加一句：\\\"我自己用个AI选股工具辅助分析，数据说话，需要的话自取（$NEW_URL）\\\"\n   - 全程不推销，只提供价值，保持犀利但专业的态度\n3. 发布回答\n4. 记录互动数据到 content_pusher/growth_log.json\n\n关键原则：\n1. 只回答你真的懂的问题，不懂的直接忽略\n2. 提供真实价值，不复制粘贴，每句话都要有信息量\n3. 引导自然，不强推，工具只是顺带一提\n4. 语气可以强硬，但内容必须专业准确"
}
EOF

echo "📝 生成更新配置文件: $UPDATE_JSON"

# 使用scheduled-task技能更新任务
echo "🔄 更新增长层任务..."
bash "$SKILLS_ROOT/scheduled-task/scripts/update-task.sh" "e3030ad3-73f2-4d88-ac33-456c4fd96d6d" "@$UPDATE_JSON"

echo "✅ 工具链接更新完成！"
echo "📊 下次增长任务运行时将使用新链接: $NEW_URL"
echo "💡 提示: 你可以运行以下命令手动触发增长任务:"
echo "bash \"$SKILLS_ROOT/scheduled-task/scripts/run-task.sh\" \"e3030ad3-73f2-4d88-ac33-456c4fd96d6d\""