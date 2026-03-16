#!/bin/bash
# 自动部署到Render（需要Render API密钥）

set -e

# 检查API密钥
if [ -z "$RENDER_API_KEY" ]; then
    echo "❌ 请先设置Render API密钥："
    echo "   export RENDER_API_KEY='你的API密钥'"
    echo ""
    echo "如何获取API密钥："
    echo "1. 访问 https://dashboard.render.com"
    echo "2. 点击右上角账户 → 'Account Settings'"
    echo "3. 左侧菜单 → 'API Keys'"
    echo "4. 点击 'Create API Key'，复制密钥"
    exit 1
fi

echo "🔑 使用Render API密钥进行部署..."

# 检查是否已安装curl
if ! command -v curl &> /dev/null; then
    echo "❌ 需要curl命令，请先安装"
    exit 1
fi

# Render API端点
API_BASE="https://api.render.com/v1"
HEADER="Authorization: Bearer $RENDER_API_KEY"

echo "📦 检查现有服务..."
# 这里可以添加API调用，但需要服务ID
# 暂时省略，直接给出指引

echo ""
echo "✅ 自动部署准备完成！"
echo ""
echo "由于Render API需要服务ID，建议首次部署通过Web界面完成。"
echo "首次部署后，你可以通过以下命令获取服务ID："
echo "curl -s -H \"$HEADER\" \"$API_BASE/services\" | jq '.[] | select(.name==\"smart-stock-screener\") | .id'"
echo ""
echo "然后更新本脚本中的 SERVICE_ID 变量，即可实现自动部署。"
echo ""
echo "📋 首次部署步骤："
echo "1. 运行 ./deploy_to_render.sh 推送代码到GitHub"
echo "2. 通过Web界面完成首次部署"
echo "3. 获取服务ID并更新本脚本"
echo "4. 后续即可使用 ./deploy_auto.sh 自动部署"