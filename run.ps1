# Config
$WorkDir = "var"
$ContainingDirectory = Split-Path -Path $PSScriptRoot -Leaf
$PythonScript = "$ContainingDirectory/main.py"  # Specify the Python script to run

# Internal Config for Winpython64-3.12.8.0dot
$WpyFolder = "WPy64-31280"
$PyExe = Join-Path -Path $WorkDir -ChildPath "$WpyFolder\python\python.exe"
$PythonUrl = "https://github.com/winpython/winpython/releases/download/11.2.20241228final/Winpython64-3.12.8.0dot.exe"
$PythonInstaller = Join-Path -Path $WorkDir -ChildPath "Winpython64-3.12.8.0dot.exe"

# Check if setup is already done
Set-Location $PSScriptRoot
if (-Not (Test-Path $PyExe)) {
    Write-Host "Setup not found. Proceeding with setup..."
    
    if (-Not (Test-Path $WorkDir)) {
        New-Item -ItemType Directory -Path $WorkDir -Force
    }

    # Download Python installer
    Write-Host "Downloading Python..."
    Invoke-WebRequest -Uri $PythonUrl -OutFile $PythonInstaller
    
    # Run the installer to extract Python
    Write-Host "Extracting Python..."
    Start-Process -FilePath $PythonInstaller -ArgumentList "-o $PythonExtractPath -y" -Wait

    # Create a virtual environment
    Write-Host "Creating virtual environment with python $PyExe..."    
    & $PyExe -m pip install -r .\requirements.txt --no-warn-script-location

    Write-Host "Setup complete!"
}

# Run the Python script
Write-Host "Running Python script: $PythonScript..."
& $PyExe $PythonScript $args
