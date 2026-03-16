#!/bin/bash
# 发布文章到知乎
# 使用前请先保存知乎登录凭证：echo "你的密码" | agent-browser auth save zhihu --url https://www.zhihu.com --username 你的邮箱 --password-stdin

set -e  # 出错时退出

# 检查参数
if [ $# -lt 1 ]; then
    echo "使用方法: $0 <文章文件路径>"
    exit 1
fi

ARTICLE_FILE="$1"

# 检查文件是否存在
if [ ! -f "$ARTICLE_FILE" ]; then
    echo "错误: 文件不存在: $ARTICLE_FILE"
    exit 1
fi

# 读取文章内容
ARTICLE_CONTENT=$(cat "$ARTICLE_FILE")
# 提取标题（第一行，去掉#和空格）
TITLE=$(head -n 1 "$ARTICLE_FILE" | sed 's/^# //')

echo "准备发布文章到知乎: $TITLE"

# 使用agent-browser登录知乎
echo "登录知乎..."
agent-browser auth login zhihu

# 打开知乎发布页面
echo "打开知乎发布页面..."
agent-browser open https://zhuanlan.zhihu.com/write

# 等待页面加载
agent-browser wait --load networkidle

# 截图以便调试
agent-browser screenshot --annotate zhihu_publish_page.png

# 获取页面元素引用
echo "获取页面元素..."
agent-browser snapshot -i

# 填写标题（假设标题输入框是@e1，实际情况可能需要调整）
echo "填写标题: $TITLE"
agent-browser fill @e1 "$TITLE"

# 填写正文（假设正文编辑器是@e2）
echo "填写正文..."
# 可能需要先点击编辑器激活
agent-browser click @e2
# 使用键盘插入文本（避免富文本编辑器问题）
agent-browser keyboard inserttext "$ARTICLE_CONTENT"

# 选择话题（假设话题输入框是@e3）
echo "添加话题..."
agent-browser click @e3
agent-browser keyboard inserttext "A股投资"
agent-browser press Enter
agent-browser keyboard inserttext "量化分析"
agent-browser press Enter
agent-browser keyboard inserttext "免费工具"
agent-browser press Enter

# 发布按钮（假设是@e4）
echo "点击发布..."
agent-browser click @e4

# 等待发布完成
agent-browser wait --url "**/p/**"

echo "文章发布成功！"
agent-browser get url