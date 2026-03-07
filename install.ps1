# Adam Skills Installer
# Run from the adam-skills repo root
# Usage: .\install.ps1

param(
    [string]$SkillsPath = "$env:USERPROFILE\.openclaw\workspace\skills",
    [string[]]$Skills = @()
)

$REPO_ROOT = $PSScriptRoot
$ALL_SKILLS = @("weather","news-headlines","notes","morning-briefing","email-intelligence","inner-eye","presence-pulse","synthesis","contractor-prospector","nano-banana-pro")

Write-Host ""
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "  Adam Skills Installer" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""

# Show menu if no skills specified
if ($Skills.Count -eq 0) {
    Write-Host "Available skills:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "  CORE (zero config)"
    Write-Host "    1. weather          - Current conditions + forecast"
    Write-Host "    2. news-headlines   - Top headlines via RSS"
    Write-Host "    3. notes            - Save notes to your vault"
    Write-Host "    4. morning-briefing - Weather + news + email in one shot"
    Write-Host ""
    Write-Host "  INTELLIGENCE (uses your existing tools)"
    Write-Host "    5. email-intelligence - Proactive email triage + alerts"
    Write-Host "    6. synthesis          - Latent pattern recognition"
    Write-Host "    7. presence-pulse     - Session resonance continuity"
    Write-Host "    8. inner-eye          - Screen + webcam vision (needs Gemini key)"
    Write-Host ""
    Write-Host "  ACTION"
    Write-Host "    9. contractor-prospector - Lead gen + site build + outreach"
    Write-Host "   10. nano-banana-pro       - AI image generation (needs billing)"
    Write-Host ""
    Write-Host "   all - Install everything"
    Write-Host ""
    $input = Read-Host "Which skills? (e.g. '1 2 3' or 'all')"
    
    if ($input -eq "all") {
        $Skills = $ALL_SKILLS
    } else {
        $nums = $input.Trim().Split(" ") | Where-Object { $_ -match "^\d+$" } | ForEach-Object { [int]$_ }
        $Skills = $nums | ForEach-Object {
            if ($_ -ge 1 -and $_ -le $ALL_SKILLS.Count) { $ALL_SKILLS[$_ - 1] }
        }
    }
}

if ($Skills.Count -eq 0) {
    Write-Host "No skills selected. Exiting." -ForegroundColor Red
    exit
}

# Install selected skills
Write-Host ""
Write-Host "Installing to: $SkillsPath" -ForegroundColor Green
Write-Host ""

foreach ($skill in $Skills) {
    $src = Join-Path $REPO_ROOT "skills\$skill"
    $dest = Join-Path $SkillsPath $skill
    
    if (-not (Test-Path $src)) {
        Write-Host "  ⚠  $skill - not found in repo, skipping" -ForegroundColor Yellow
        continue
    }
    
    if (Test-Path $dest) {
        Write-Host "  ↻  $skill - already installed, updating..." -ForegroundColor Cyan
    } else {
        Write-Host "  +  $skill - installing..." -ForegroundColor Green
    }
    
    Copy-Item -Recurse -Force $src $dest
    Write-Host "     ✓ Done → $dest" -ForegroundColor Gray
}

Write-Host ""
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "  Installation complete." -ForegroundColor Cyan
Write-Host ""
Write-Host "  Next: Restart your OpenClaw gateway so Adam" -ForegroundColor White
Write-Host "  picks up the new skills." -ForegroundColor White
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""
