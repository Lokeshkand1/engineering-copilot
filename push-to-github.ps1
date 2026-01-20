# GitHub Push Script for Engineering Copilot

Write-Host "`n=== Engineering Copilot - GitHub Push ===" -ForegroundColor Cyan
Write-Host "`nPushing your Engineering Copilot project to GitHub...`n" -ForegroundColor Yellow

# Get GitHub username
$username = Read-Host "Enter your GitHub username"

# Get repository name
$repoName = Read-Host "Enter repository name (press Enter for 'engineering-copilot')"
if ([string]::IsNullOrWhiteSpace($repoName)) {
    $repoName = "engineering-copilot"
}

Write-Host "`n--- Create GitHub Repository First ---" -ForegroundColor Green
Write-Host "1. Go to https://github.com/new" -ForegroundColor White
Write-Host "2. Repository name: $repoName" -ForegroundColor White
Write-Host "3. Description: AI-powered engineering assistant for structural analysis and material selection" -ForegroundColor White
Write-Host "4. Choose Public or Private" -ForegroundColor White
Write-Host "5. DO NOT initialize with README, .gitignore, or license" -ForegroundColor Yellow
Write-Host "6. Click 'Create repository'" -ForegroundColor White
Write-Host "`nPress Enter after creating the repository on GitHub..." -ForegroundColor Cyan
$null = Read-Host

# Add remote
$remoteUrl = "https://github.com/$username/$repoName.git"
Write-Host "`nAdding remote: $remoteUrl" -ForegroundColor Cyan
& 'C:\Program Files\Git\bin\git.exe' remote add origin $remoteUrl

# Rename branch to main
Write-Host "Setting branch to main..." -ForegroundColor Cyan
& 'C:\Program Files\Git\bin\git.exe' branch -M main

# Push to GitHub
Write-Host "`nPushing to GitHub..." -ForegroundColor Cyan
Write-Host "Note: You'll need a Personal Access Token (not password)" -ForegroundColor Yellow
Write-Host "Get one at: https://github.com/settings/tokens" -ForegroundColor White
Write-Host "`n"

& 'C:\Program Files\Git\bin\git.exe' push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n=== SUCCESS! ===" -ForegroundColor Green
    Write-Host "Your Engineering Copilot is now on GitHub!" -ForegroundColor Green
    Write-Host "`nView at: https://github.com/$username/$repoName" -ForegroundColor Cyan
    Write-Host "`nShare this link in your P-1 AI application! 🚀" -ForegroundColor Yellow
}
else {
    Write-Host "`n=== ERROR ===" -ForegroundColor Red
    Write-Host "Push failed. Common issues:" -ForegroundColor Yellow
    Write-Host "1. Repository doesn't exist - create it on GitHub first" -ForegroundColor White
    Write-Host "2. Wrong username" -ForegroundColor White
    Write-Host "3. Need Personal Access Token: https://github.com/settings/tokens" -ForegroundColor White
}

Write-Host "`nPress Enter to exit..." -ForegroundColor Cyan
$null = Read-Host
