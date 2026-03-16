# Railway部署脚本
# 使用方法：
# 1. 安装Railway CLI: npm i -g @railway/cli
# 2. 登录: railway login
# 3. 运行此脚本: powershell -ExecutionPolicy Bypass -File deploy_railway.ps1

Write-Host "智能选股工具Railway部署脚本" -ForegroundColor Green
Write-Host "========================================="

# 检查Railway CLI是否安装
try {
    $railwayVersion = railway --version
    Write-Host "✅ Railway CLI已安装: $railwayVersion"
} catch {
    Write-Host "❌ Railway CLI未安装" -ForegroundColor Red
    Write-Host "请运行: npm i -g @railway/cli"
    exit 1
}

# 检查是否登录
Write-Host "检查Railway登录状态..."
$loginStatus = railway whoami 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ 未登录Railway" -ForegroundColor Red
    Write-Host "请运行: railway login"
    exit 1
} else {
    Write-Host "✅ 已登录Railway: $loginStatus"
}

# 初始化项目（如果尚未初始化）
if (!(Test-Path ".railway")) {
    Write-Host "初始化Railway项目..."
    railway init --name "smart-stock-screener" --environment production
} else {
    Write-Host "✅ Railway项目已初始化"
}

# 设置环境变量（如果需要）
Write-Host "设置环境变量..."
railway variables set PORT=5000
railway variables set FLASK_ENV=production

# 部署到Railway
Write-Host "开始部署到Railway..." -ForegroundColor Yellow
railway up --service smart-stock-screener

Write-Host "✅ 部署完成！" -ForegroundColor Green
Write-Host "使用以下命令查看部署状态: railway status"
Write-Host "打开Web界面: railway open"