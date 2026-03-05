# Redirect Multipass + Hyper-V storage to J:\gus-engine
# MUST be run as Administrator

$storagePath = "J:\gus-engine"

Write-Host "=== Redirecting Multipass storage to $storagePath ===" -ForegroundColor Cyan

# 1. Stop Multipass service
Write-Host "`n[1/5] Stopping Multipass service..."
Stop-Service Multipass -Force
Start-Sleep -Seconds 2

# 2. Create storage directory
Write-Host "[2/5] Creating storage directory..."
New-Item -ItemType Directory -Force -Path $storagePath | Out-Null

# 3. Set MULTIPASS_STORAGE in registry (system-level environment variable)
Write-Host "[3/5] Setting MULTIPASS_STORAGE registry key..."
Set-ItemProperty -Path "HKLM:\System\CurrentControlSet\Control\Session Manager\Environment" -Name MULTIPASS_STORAGE -Value $storagePath

# 4. Copy existing Multipass data (if any)
$sourceData = "C:\ProgramData\Multipass"
if (Test-Path $sourceData) {
    Write-Host "[4/5] Copying existing Multipass data to new location..."
    Copy-Item -Path "$sourceData\*" -Recurse -Force -Destination $storagePath
}
else {
    Write-Host "[4/5] No existing Multipass data to copy (clean install)."
}

# 5. Also set Hyper-V default paths to J: drive
Write-Host "[5/5] Redirecting Hyper-V default VM storage paths..."
$hvVMPath = "$storagePath\Hyper-V\Virtual Machines"
$hvVHDPath = "$storagePath\Hyper-V\Virtual Hard Disks"
New-Item -ItemType Directory -Force -Path $hvVMPath | Out-Null
New-Item -ItemType Directory -Force -Path $hvVHDPath | Out-Null
Set-VMHost -VirtualMachinePath $hvVMPath -VirtualHardDiskPath $hvVHDPath

# 6. Restart Multipass
Write-Host "`nStarting Multipass service..."
Start-Service Multipass
Start-Sleep -Seconds 3

# Verify
Write-Host "`n=== Verification ===" -ForegroundColor Green
Write-Host "Multipass Service: $((Get-Service Multipass).Status)"
Write-Host "MULTIPASS_STORAGE: $((Get-ItemProperty 'HKLM:\System\CurrentControlSet\Control\Session Manager\Environment').MULTIPASS_STORAGE)"
$vmHost = Get-VMHost
Write-Host "Hyper-V VM Path:   $($vmHost.VirtualMachinePath)"
Write-Host "Hyper-V VHD Path:  $($vmHost.VirtualHardDiskPath)"
Write-Host "`n=== Done! You can now launch: ===" -ForegroundColor Green
Write-Host "multipass launch 22.04 --name gus-engine --cpus 4 --memory 32G --disk 150G" -ForegroundColor Yellow
