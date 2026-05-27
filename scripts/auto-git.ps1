$root = (Get-Item -LiteralPath "$PSScriptRoot\..").FullName
$watcher = New-Object System.IO.FileSystemWatcher
$watcher.Path = $root
$watcher.IncludeSubdirectories = $true
$watcher.NotifyFilter = [System.IO.NotifyFilters]::FileName -bor [System.IO.NotifyFilters]::DirectoryName -bor [System.IO.NotifyFilters]::LastWrite
$watcher.EnableRaisingEvents = $true

$ignoreDirs = @('.git', '__pycache__', '.venv', 'venv', 'env', '.vscode', '.idea', '.agents', 'opencode-skillful-main', '.memory', 'node_modules')
$ignoreExt = @('.log', '.db', '.sqlite', '.sqlite3', '.pyc', '.pyo', '.egg', '.whl')

$changed = $false
$lastChange = [DateTime]::MinValue

$action = {
    $path = $Event.SourceEventArgs.FullPath
    $relative = $path.Substring(($watcher.Path.Length + 1))
    $parts = $relative -split '\\'

    foreach ($dir in $ignoreDirs) {
        if ($parts -contains $dir) { return }
    }
    foreach ($ext in $ignoreExt) {
        if ($relative -like ('*' + $ext)) { return }
    }

    $script:changed = $true
    $script:lastChange = [DateTime]::Now
}

Register-ObjectEvent -InputObject $watcher -EventName Created -Action $action > $null
Register-ObjectEvent -InputObject $watcher -EventName Changed -Action $action > $null
Register-ObjectEvent -InputObject $watcher -EventName Deleted -Action $action > $null
Register-ObjectEvent -InputObject $watcher -EventName Renamed -Action $action > $null

Write-Host "Auto-git is running. Watching: $root"
Write-Host "Press Ctrl+C to stop."

while ($true) {
    Start-Sleep -Milliseconds 1000

    if (-not $changed) { continue }
    $elapsed = [DateTime]::Now - $lastChange
    if ($elapsed.TotalSeconds -lt 4) { continue }

    $script:changed = $false
    Write-Host ("[{0:HH:mm:ss}] Changes detected. Committing and pushing..." -f [DateTime]::Now)

    try {
        Push-Location $root
        git add -A 2>&1 | Out-Null
        $diff = git diff --cached --name-only
        if ($diff) {
            $msg = "auto-commit: " + ($diff -join ', ')
            if ($msg.Length -gt 100) { $msg = $msg.Substring(0, 97) + '...' }
            git commit -m $msg 2>&1 | Out-Null
            $pushResult = git push origin master 2>&1
            Write-Host ("[{0:HH:mm:ss}] Pushed to GitHub" -f [DateTime]::Now)
        } else {
            Write-Host ("[{0:HH:mm:ss}] Nothing to commit" -f [DateTime]::Now)
        }
        Pop-Location
    } catch {
        $err = $_.Exception.Message
        Write-Host ("[ERROR] {0}" -f $err) -ForegroundColor Red
    }
}
