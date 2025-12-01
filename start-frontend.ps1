#!/usr/bin/env pwsh
# start-frontend.ps1
# Starts the React frontend. If npm isn't on PATH, tries common node installation path.

Param(
    [string]$ProjectDir = "$PSScriptRoot\frontend"
)

Push-Location $ProjectDir

function Try-Start {
    Write-Host "Starting frontend in: $ProjectDir"
    if (Get-Command npm -ErrorAction SilentlyContinue) {
        npm install
        npm start
        return $true
    }

    # Try direct path to npm.cmd where Node is typically installed
    $npmCmd = 'C:\Program Files\nodejs\npm.cmd'
    if (Test-Path $npmCmd) {
        & $npmCmd install
        & $npmCmd start
        return $true
    }

    # Try temporarily adding Program Files\nodejs to PATH for this session
    $nodePath = 'C:\Program Files\nodejs'
    if (Test-Path $nodePath) {
        $env:PATH = "$nodePath;" + $env:PATH
        if (Get-Command npm -ErrorAction SilentlyContinue) {
            npm install
            npm start
            return $true
        }
    }

    Write-Error "npm not found. Please install Node.js and ensure npm is on PATH."
    return $false
}

Try-Start

Pop-Location
