$json = Get-Content 'C:\Users\ajsup\.openclaw\openclaw.json' -Raw | ConvertFrom-Json
$token = $json.env.GITHUB_SAM_TOKEN

$headers = @{
    Authorization = "token $token"
    Accept = "application/vnd.github+json"
}
$body = '{"name":"adam-skills","description":"Official skill library for the Adam Framework","private":false,"auto_init":false}'

$response = Invoke-RestMethod -Uri "https://api.github.com/orgs/strangeadvancedmarketing/repos" -Method Post -Headers $headers -Body $body -ContentType "application/json"
Write-Host "Repo created: $($response.html_url)"

cd C:\Users\ajsup\adam-skills
git remote remove origin 2>$null
git remote add origin "https://$($token)@github.com/strangeadvancedmarketing/adam-skills.git"
git push -u origin master 2>&1
Write-Host "Push done"
