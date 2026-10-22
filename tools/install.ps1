# Install jinzhongzi-cup skill into a local Agent Skills directory.
#
# Usage (PowerShell):
#   .\tools\install.ps1                      # copy into <repo>/.dsh/skills
#   .\tools\install.ps1 -Target dsh          # <project>/.dsh/skills
#   .\tools\install.ps1 -Target agents       # ~/.agents/skills
#   .\tools\install.ps1 -Target claude       # ~/.claude/skills
#   .\tools\install.ps1 -Dest D:\path\skills # custom root
#   .\tools\install.ps1 -Force               # overwrite existing copy
#
# The skill directory name must equal the skill `name` in SKILL.md (jinzhongzi-cup).

[CmdletBinding()]
param(
    [ValidateSet('dsh', 'agents', 'claude', 'project')]
    [string]$Target = 'dsh',
    [string]$Dest,
    [switch]$Force
)

$ErrorActionPreference = 'Stop'
$repo = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$src = Join-Path $repo 'skills\jinzhongzi-cup'
if (-not (Test-Path (Join-Path $src 'SKILL.md'))) {
    throw "找不到 skills\jinzhongzi-cup\SKILL.md，请从仓库根目录运行本脚本。"
}

if (-not $Dest) {
    switch ($Target) {
        'dsh' { $Dest = Join-Path (Get-Location) '.dsh\skills' }
        'project' { $Dest = Join-Path (Get-Location) '.dsh\skills' }
        'agents' { $Dest = Join-Path $HOME '.agents\skills' }
        'claude' { $Dest = Join-Path $HOME '.claude\skills' }
    }
}

$out = Join-Path $Dest 'jinzhongzi-cup'
if ((Test-Path $out) -and -not $Force) {
    Write-Host "已存在：$out（加 -Force 覆盖）" -ForegroundColor Yellow
    exit 0
}

New-Item -ItemType Directory -Force -Path $Dest | Out-Null
if (Test-Path $out) { Remove-Item -Recurse -Force $out }
Copy-Item -Recurse $src $out

$files = (Get-ChildItem -Recurse -File $out | Measure-Object).Count
Write-Host "已安装到：$out（$files 个文件）" -ForegroundColor Green
Write-Host "验证：python tools/validate_skill.py `"$Dest`"" -ForegroundColor DarkGray
Write-Host "新开会话后可用 /jinzhongzi-cup，或让助手自动加载。" -ForegroundColor DarkGray
