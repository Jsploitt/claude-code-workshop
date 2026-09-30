$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot
$claude = Join-Path $env:USERPROFILE ".local\bin\claude.exe"
if (-not (Test-Path $claude)) { $claude = "claude" }
$raw = & $claude -p "/scout" --allowedTools "WebSearch,WebFetch,Read" --output-format json
$raw | Out-File -Encoding utf8 last_run.json
python render.py last_run.json @args
