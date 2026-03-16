#!/bin/bash
# 部署智能选股工具到Render

set -e  # 出错时停止

echo "🚀 开始部署智能选股工具到Render..."

# 步骤1: 检查Git仓库
if [ ! -d ".git" ]; then
    echo "📦 初始化Git仓库..."
    git init
    git add .
    git commit -m "Initial commit: 智能选股工具"
    echo "✅ Git仓库初始化完成"
else
    echo "✅ Git仓库已存在"
fi

# 步骤2: 检查是否有远程仓库
REMOTE_URL=$(git remote get-url origin 2>/dev/null || echo "")
if [ -z "$REMOTE_URL" ]; then
    echo "⚠️  请先在GitHub上创建新仓库，然后运行以下命令："
    echo "   git remote add origin <你的GitHub仓库URL>"
    echo "   git push -u origin main"
    echo ""
    echo "或者，如果你使用GitHub CLI，可以运行："
    echo "   gh repo create stock-screener --public --source=. --remote=origin --push"
    exit 1
else
    echo "✅ 远程仓库已配置: $REMOTE_URL"
fi

# 步骤3: 推送到GitHub
echo "📤 推送到GitHub..."
git push origin main

echo ""
echo "=========================================="
echo "🎉 本地代码已推送到GitHub!"
echo ""
echo "接下来请在Render完成部署："
echo "1. 访问 https://dashboard.render.com"
echo "2. 点击 'New +' → 'Web Service'"
echo "3. 连接你的GitHub仓库"
echo "4. 选择本仓库 (stock-screener)"
echo "5. 服务名称: smart-stock-screener"
echo "6. 点击 'Create Web Service'"
echo "7. 等待部署完成（约2-3分钟）"
echo "8. 获取你的公开URL（格式如：https://smart-stock-screener.onrender.com）"
echo "=========================================="
echo ""
echo "部署完成后，你可以通过以下命令测试服务："
echo "curl https://smart-stock-screener.onrender.com/api/health"
echo ""
echo "📝 后续自动化："
echo "保存Render API密钥以启用自动化："
echo "export RENDER_API_KEY='你的API密钥'"
echo "./deploy_auto.sh"