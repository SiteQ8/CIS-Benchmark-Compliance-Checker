# Windows Server CIS Benchmark Checks
# Author: SiteQ8
# Description: PowerShell-based compliance checks for Windows Server

Write-Host "=== Windows Server CIS Benchmark Compliance Checks ===" -ForegroundColor Cyan
Write-Host ""

# 1.1.1 - Check password history
Write-Host "[1.1.1] Checking password history policy..." -ForegroundColor Yellow
$pwHistory = (net accounts | Select-String "Length of password history").ToString().Split(":")[-1].Trim()
if ([int]$pwHistory -ge 24) {
    Write-Host "✅ PASS: Password history is $pwHistory" -ForegroundColor Green
} else {
    Write-Host "❌ FAIL: Password history is $pwHistory (should be >= 24)" -ForegroundColor Red
}

# 2.2.1 - Check Windows Firewall
Write-Host "[2.2.1] Checking Windows Firewall status..." -ForegroundColor Yellow
$fwProfiles = @("Domain", "Private", "Public")
$allEnabled = $true
foreach ($profile in $fwProfiles) {
    $status = (Get-NetFirewallProfile -Name $profile).Enabled
    if ($status) {
        Write-Host "  ✅ $profile profile is enabled" -ForegroundColor Green
    } else {
        Write-Host "  ❌ $profile profile is disabled" -ForegroundColor Red
        $allEnabled = $false
    }
}

if ($allEnabled) {
    Write-Host "✅ PASS: All firewall profiles are enabled" -ForegroundColor Green
} else {
    Write-Host "❌ FAIL: Some firewall profiles are disabled" -ForegroundColor Red
}

Write-Host ""
Write-Host "=== Compliance Check Completed ===" -ForegroundColor Cyan
