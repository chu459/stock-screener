#!/bin/bash
SKILLS_ROOT="C:/Users/17632/AppData/Roaming/LobsterAI/SKILLs"
SEARCH_SCRIPT="$SKILLS_ROOT/web-search/scripts/search.sh"

# 创建输出目录
OUTPUT_DIR="./research_results"
mkdir -p "$OUTPUT_DIR"

# 搜索函数
search_and_save() {
    local query="$1"
    local filename="$2"
    local max_results="${3:-5}"
    echo "搜索: $query"
    bash "$SEARCH_SCRIPT" "$query" "$max_results" > "$OUTPUT_DIR/$filename.md" 2>&1
    echo "保存到: $OUTPUT_DIR/$filename.md"
}

# 1. 知乎高流量文章写作技巧
search_and_save "知乎 高流量文章 写作技巧 2026" "zhihu_high_traffic"

# 2. 知乎金融投资高赞文章案例
search_and_save "知乎 金融投资 高赞文章 案例 2026" "zhihu_finance_articles"

# 3. 智能选股工具推广知乎文章
search_and_save "智能选股 工具 推广 知乎 文章" "zhihu_promotion"

# 4. 知乎高转化率文章特点
search_and_save "知乎 转化率 高 文章 特点" "zhihu_conversion"

# 5. 股票筛选工具用户需求
search_and_save "股票筛选 工具 用户需求 2026" "user_needs"

# 6. 知乎文章标题技巧
search_and_save "知乎 文章 标题 技巧 吸引点击" "zhihu_titles"

# 7. 投资类知乎大V分析
search_and_save "投资 类 知乎 大V 文章 风格" "zhihu_influencers"

# 8. 免费工具推广策略
search_and_save "免费 工具 推广 策略 知乎" "free_tool_promotion"

echo "所有搜索完成。结果保存在 $OUTPUT_DIR 目录中。"