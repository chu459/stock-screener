# 智能选股工具部署指南

## 当前状态
✅ 本地服务运行正常 (http://localhost:5000)
✅ Git仓库已初始化并提交
✅ 增长任务已配置但使用localhost链接（转化率0%）

## 部署目标
获取公共URL，替换增长任务中的 `http://localhost:5000`，实现点击→访问→转化的完整漏斗。

## 推荐方案：Render.com（免费，稳定）

### 步骤1：创建GitHub仓库
1. 访问 https://github.com/new
2. 仓库名: `smart-stock-screener`
3. 描述: "AI智能选股工具 - Flask应用"
4. **不要**添加README、.gitignore、license（本地已有）
5. 创建仓库
6. 复制仓库SSH/HTTPS URL

### 步骤2：推送代码到GitHub
```bash
# 在 stock_screener 目录中执行
git remote add origin <你的仓库URL>
git push -u origin main
```

### 步骤3：部署到Render
1. 访问 https://dashboard.render.com
2. 点击 "New +" → "Web Service"
3. 连接GitHub账户，选择 `smart-stock-screener` 仓库
4. 配置服务：
   - **Name**: `smart-stock-screener`
   - **Region**: Singapore (或离你近的)
   - **Branch**: `main`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: Free
5. 点击 "Create Web Service"
6. 等待部署完成（约3-5分钟）
7. 获取公共URL：`https://smart-stock-screener.onrender.com`

### 步骤4：更新增长任务链接
```bash
# 在 stock_screener 目录中执行
./update_tool_url.sh https://smart-stock-screener.onrender.com
```

## 备选方案：Railway.app
1. 安装Railway CLI: `npm i -g @railway/cli`
2. 登录: `railway login`
3. 部署: `powershell -ExecutionPolicy Bypass -File deploy_railway.ps1`
4. 获取URL后运行: `./update_tool_url.sh <你的URL>`

## 验证部署
1. 访问你的公共URL
2. 点击"筛选"按钮，确认功能正常
3. 手动触发增长任务测试：
   ```bash
   bash "$SKILLS_ROOT/scheduled-task/scripts/run-task.sh" "e3030ad3-73f2-4d88-ac33-456c4fd96d6d"
   ```
4. 检查 [growth_log.json](file:///C:/Users/17632/lobsterai/project/content_pusher/growth_log.json) 的转化数据

## 预期结果
- 增长任务继续每30分钟提供价值
- 用户点击工具链接 → 访问公共URL → 使用工具
- 转化率从0%开始提升
- 全系统7×24h自动化运行，你只需等转化数据

## 故障排除
- **部署失败**: 检查 `requirements.txt` 中的依赖版本
- **服务无法启动**: 查看Render/Railway日志
- **链接不更新**: 确认 `update_tool_url.sh` 执行成功
- **转化率仍为0**: 确认公共URL可访问，工具功能正常

## 下一步
部署完成后，系统将形成完整闭环：
1. 研究层 → 发现痛点
2. 内容层 → 生成针对性内容
3. 增长层 → 在社区提供价值+工具链接
4. 用户 → 点击→访问→使用→自然转化
5. 监控层 → 确保服务健康

**你只需等待转化数据，系统全自动运行。**