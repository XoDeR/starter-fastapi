$ErrorActionPreference = "Stop"

# Tilt cannot set its web UI port from the Tiltfile. Default 10350 is already
# used on this machine, so this project always binds 10360.
$tiltPort = 10360
$env:TILT_PORT = "$tiltPort"

Write-Host "Starting Tilt UI at http://localhost:$tiltPort/"
tilt up --port $tiltPort @args
