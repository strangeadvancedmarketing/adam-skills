# Adam Skills Installer
# Run from the adam-skills repo root
# Usage: .\install.ps1

param(
    [string]$SkillsPath = "$env:USERPROFILE\.openclaw\workspace\skills",
    [string[]]$Skills = @()
)

$REPO_ROOT = $PSScriptRoot
$ALL_SKILLS = @(
    "weather",
    "news-headlines",
    "notes",
    "morning-briefing",
    "system-health",
    "uptime-check",
    "email-intelligence",
    "inner-eye",
    "presence-pulse",
    "synthesis",
    "contractor-prospector",
    "nano-banana-pro"
)

Write-Host ""
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "  Adam Skills Installer" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""

if ($Skills.Count -eq 0) {
    Write-Host "Available skills:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "  CORE (zero config)"
    Write-Host "    1. weather             Current conditions + forecast"
    Write-Host "    2. news-headlines      Top headlines via RSS"
    Write-Host "    3. notes               Save notes to your vault"
    Write-Host "    4. morning-briefing    Weather + news + email in one shot"
    Write-Host "    5. system-health       CPU, RAM, disk, top processes  [pip install psutil]"
    Write-Host "    6. uptime-check        Ping your live endpoints"
    Write-Host ""
    Write-Host "  INTELLIGENCE (uses your existing tools)"
    Write-Host "    7. email-intelligence  Proactive email triage + Telegram alerts"
    Write-Host "    8. inner-eye           Screen + webcam vision via Gemini"
    Write-Host "    9. presence-pulse      Session resonance continuity"
    Write-Host "   10. synthesis           Latent pattern recognition"
    Write-Host ""
    Write-Host "  ACTION"
    Write-Host "   11. contractor-prospector  Lead gen + site build + outreach"
    Write-Host "   12. nano-banana-pro        AI image generation (needs billing)"
    Write-Host ""
    Write-Host "   all - Install everything"
    Write-Host ""
    $input = Read-Host "Which skills? (e.g. '1 2 3' or 'all')"

    if ($input.Trim() -eq "all") {
        $Skills = $ALL_SKILLS
    } else {
        $nums = $input.Trim().Split(" ") | Where-Object { $_ -match "^\d+$" } | ForEach-Object { [int]$_ }
        $Skills = $nums | ForEach-Object {
            if ($_ -ge 1 -and $_ -le $ALL_SKILLS.Count) { $ALL_SKILLS[$_ - 1] }
        } | Where-Object { $_ }
    }
}

if ($Skills.Count -eq 0) {
    Write-Host "No skills selected. Exiting." -ForegroundColor Red
    exit
}

Write-Host ""
Write-Host "Installing to: $SkillsPath" -ForegroundColor Green
Write-Host ""

foreach ($skill in $Skills) {
    $src  = Join-Path $REPO_ROOT "skills\$skill"
    $dest = Join-Path $SkillsPath $skill

    if (-not (Test-Path $src)) {
        Write-Host "  ⚠  $skill - not found in repo, skipping" -ForegroundColor Yellow
        continue
    }

    if (Test-Path $dest) {
        Write-Host "  ↻  $skill - updating..." -ForegroundColor Cyan
    } else {
        Write-Host "  +  $skill - installing..." -ForegroundColor Green
    }

    Copy-Item -Recurse -Force $src $dest
    Write-Host "     ✓ $dest" -ForegroundColor Gray
}

Write-Host ""
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "  Done. Restart your OpenClaw gateway so Adam" -ForegroundColor White
Write-Host "  picks up the new skills." -ForegroundColor White
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""
