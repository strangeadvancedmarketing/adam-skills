$json = Get-Content 'C:\Users\ajsup\.openclaw\openclaw.json' -Raw | ConvertFrom-Json
$token = $json.env.GITHUB_SAM_TOKEN
$auth = "token " + $token
$r = Invoke-WebRequest -Uri "https://api.github.com/user" -Headers @{Authorization=$auth}
Write-Host "Scopes: $($r.Headers['X-OAuth-Scopes'])"
Write-Host "Login: $(($r.Content | ConvertFrom-Json).login)"
