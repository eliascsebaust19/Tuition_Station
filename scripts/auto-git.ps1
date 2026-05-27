$watcher = New-Object System.IO.FileSystemWatcher
$watcher.Path = (Get-Item -LiteralPath "$PSScriptRoot\..").FullName
$watcher.IncludeSubdirectories = $true
$watcher.EnableRaisingEvents = $true

$ignoreDirs = @('.git', '__pycache__', '.venv', 'venv', 'env', '.vscode', '.idea', '.agents', 'opencode-skillful-main', '.memory')
$ignoreExt = @('.log', '.db', '.sqlite', '.sqlite3', '.pyc', '.pyo', '.egg', '.whl')

$timer = $null
$changed = $false

$action = {
    $path = $Event.SourceEventArgs.FullPath
    $relative = $path.Substring($watcher.Path.Length + 1)
    $parts = $relative -split '\\'

    $ignore = $false
    foreach ($dir in $ignoreDirs) {
        if ($parts -contains $dir) { $ignore = $true; break }
    }
    if (-not $ignore) {
        foreach ($ext in $ignoreExt) {
            if ($relative -like "*$ext") { $ignore = $true; break }
        }
    }
    if ($ignore) { return }

    $script:changed = $true
    if ($script:timer) { $script:timer.Dispose() }
    $script:timer = [System.Timers.Timer]::new(5000)
    $script:timer.AutoReset = $false
    Register-ObjectEvent -InputObject $script:timer -EventName Elapsed -Action {
        if (-not $script:changed) { return }
        $script:changed = $false
        $dir = $watcher.Path
        Write-Host "[$(Get-Date -Format 'HH:mm:ss')] Changes detected. Committing and pushing..."
        try {
            Push-Location $dir
            git add -A 2>&1 | Out-Null
            $diff = git diff --cached --name-only
            if ($diff) {
                $msg = "auto-commit: " + ($diff -join ', ')
                if ($msg.Length -gt 100) { $msg = $msg.Substring(0, 97) + "..." }
                git commit -m $msg 2>&1 | Out-Null
                git push origin master 2>&1 | Out-Null
                Write-Host "[$(Get-Date -Format 'HH:mm:ss')] Committed and pushed to GitHub ✓"
            }
            Pop-Location
        } catch {
            Write-Host "[ERROR] $_" -ForegroundColor Red
        }
    } | Out-Null
    $script:timer.Start()
}

Register-ObjectEvent -InputObject $watcher -EventName Created -Action $action | Out-Null
Register-ObjectEvent -InputObject $watcher -EventName Changed -Action $action | Out-Null
Register-ObjectEvent -InputObject $watcher -EventName Deleted -Action $action | Out-Null
Register-ObjectEvent -InputObject $watcher -EventName Renamed -Action $action | Out-Null

Write-Host "Auto-git is running. Watching for changes in: $($watcher.Path)"
Write-Host "Press Ctrl+C to stop."
while ($true) { Start-Sleep -Seconds 1 }
