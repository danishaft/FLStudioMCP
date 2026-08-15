# setup-windows.ps1 — Windows-side setup after install
# Run in PowerShell as Administrator

$ErrorActionPreference = "Stop"

Write-Host "=== FL Studio CLI — Windows Setup ===" -ForegroundColor Cyan

# Find SHARED partition
Write-Host "`n[1/6] Finding SHARED partition..."
$shared = Get-Volume | Where-Object { $_.FileSystemLabel -eq "SHARED" }
if (-not $shared) {
    Write-Host "ERROR: No SHARED partition found. Is it mounted?" -ForegroundColor Red
    exit 1
}
$sharedDrive = $shared.DriveLetter + ":"
Write-Host "  Found: $sharedDrive"

# Create target directories
Write-Host "`n[2/6] Creating directories..."
$home = $env:USERPROFILE
$dirs = @(
    "$home\Desktop",
    "$home\.codex\agents",
    "$home\.config\opencode",
    "$home\.agents\skills"
)
foreach ($d in $dirs) {
    New-Item -ItemType Directory -Force -Path $d | Out-Null
}
Write-Host "  Done."

# Copy project files
Write-Host "`n[3/6] Copying project files..."
Copy-Item -Recurse -Force "$sharedDrive\home\ayodele\Desktop\flmcp" "$home\Desktop\flmcp"
Copy-Item -Recurse -Force "$sharedDrive\home\ayodele\.codex\agents\*" "$home\.codex\agents\"
Copy-Item -Recurse -Force "$sharedDrive\home\ayodele\.config\opencode\*" "$home\.config\opencode\"
if (Test-Path "$sharedDrive\home\ayodele\.agents\skills") {
    Copy-Item -Recurse -Force "$sharedDrive\home\ayodele\.agents\skills\*" "$home\.agents\skills\"
}
Write-Host "  Copied: flmcp/, .codex/, .config/opencode/, .agents/"

# Install Python
Write-Host "`n[4/6] Checking Python..."
$python = Get-Command python -ErrorAction SilentlyContinue
if ($python) {
    Write-Host "  Python found: $(python --version)"
} else {
    Write-Host "  Python NOT found. Install from: https://www.python.org/downloads/" -ForegroundColor Yellow
    Write-Host "  Make sure to check 'Add Python to PATH' during install."
}

# Install Go
Write-Host "`n[5/6] Checking Go..."
$go = Get-Command go -ErrorAction SilentlyContinue
if ($go) {
    Write-Host "  Go found: $(go version)"
} else {
    Write-Host "  Go NOT found. Install from: https://go.dev/dl/" -ForegroundColor Yellow
}

# Build CLI
Write-Host "`n[6/6] Building CLI..."
$flmcpDir = "$home\Desktop\flmcp"
if (Test-Path "$flmcpDir\pyproject.toml") {
    Write-Host "  Setting up Python environment..."
    Set-Location $flmcpDir
    python -m venv venv
    .\venv\Scripts\activate
    pip install -e ".[dev]"
    pip install "mcp[cli]>=1.2.0,<2.0"
    
    # Install Go + clihub
    $goInstalled = Get-Command go -ErrorAction SilentlyContinue
    if ($goInstalled) {
        go install github.com/thellimist/clihub@latest
        clihub generate
        Write-Host "  CLI built successfully."
    } else {
        Write-Host "  Install Go first, then run: clihub generate" -ForegroundColor Yellow
    }
} else {
    Write-Host "  flmcp not found at $flmcpDir" -ForegroundColor Red
}

# Verify
Write-Host "`n=== Setup Complete ===" -ForegroundColor Green
Write-Host "Next steps:"
Write-Host "  1. Install FL Studio from https://www.image-line.com/fl-studio/"
Write-Host "  2. Install FL Studio ASIO driver"
Write-Host "  3. Run: cd Desktop\flmcp && flmcp transport-status -o json"
Write-Host "  4. Open opencode and continue your session!"
