Add-Type -AssemblyName System.Windows.Forms

#
# Icon by Icons8 https://icons8.com/
#

#
# Intro
#
Write-Host "KSP2 BugPackager Installer"
Write-Host " "
Start-Sleep -Seconds 1


#
# Common Functions up here
#
function Get-FirstLine() {
    param(
        [Parameter(Mandatory = $true)]
        [string]$FilePath
    )

    $firstLine = Get-Content -Path $FilePath -TotalCount 1
    $firstLine.Trim()
}

function CreateReportDir() {
    param(
        [Parameter(Mandatory = $true)]
        [string]$SelectedPath
    )
	
    $selectedFolder = $SelectedPath
    $directoryPath = $selectedFolder, "\", "$reportDir" -join ""
    if (-not(Test-Path $directoryPath)) {
	    Write-Host "Creating folder: $directoryPath"
	    # Create the directory
	    New-Item -ItemType Directory -Path $directoryPath -Force | Out-Null
    } else
    {
    	Write-Host "Selected report folder: $selectedFolder"
    }
}

#
# Look for the Player.log
# It's in the same relative location on all systems
#
$FilePath = "$HOME\AppData\LocalLow\Intercept Games\Kerbal Space Program 2\Player.log"
if (-not(Test-Path $FilePath)) {
	Write-Host " "
	Write-Host "Player.log file missing from expected location, exiting"
	Write-Host "Expected file to be at:  $FilePath"
	Start-Sleep 60
	exit
}

#
# Find the path to the game directory
#
$firstLine = Get-FirstLine -FilePath $filePath
$folderPath = $firstLine -split "'" | Select-Object -Last 2
$folderPath = $folderPath.Replace('/', '\')

$elements = $folderPath -split "\\"
$elementsToKeep = $elements[0..($elements.Count - 4)]
$path = $elementsToKeep -join "\"

#
# This is where the files will be installed
#
$packagerPath = "$path\KSP2_BugPackager"

Write-Host "Installing KSP2 Bug Packager to directory: $packagerPath"
Write-Host " "
$yn = Read-Host -Prompt "OK to continue (press <enter> to continue, any other key to exit)"
if ($yn -ne "") {
	Write-Host "Exiting..."
	Start-Sleep -Seconds 2
	exit
}

$global:reportDir = "KSP2_BugPackagerReports"
$defaultReportLocation = "$packagerPath\$reportDir"
#
# Ask if default location for bug package files is ok
#
Write-Host " "
Write-Host " "
Write-Host "Default location for the report file is: $defaultReportLocation"
Write-Host " "
$customReportLoc = Read-Host -Prompt "Do you want to specify a custom location (enter Y for yes) ? "

#
# Create the install directory if it doesn't already exist
#
if (-not(Test-Path $packagerPath)) {
    Write-Host "Creating folder: $directoryPath"
    # Create the directory
    New-Item -ItemType Directory -Path $packagerPath -Force | Out-Null
}


#
# Copy the dist files into the install directory
#
$list = @("KSP2_BugPackager.ps1-dist", "KSP2_BugPackager.bat-dist", "KSP2_BugPackager.ico-dist")
foreach ($sourceFile in $list) {

	$destFile = $sourceFile.Replace("-dist", "")
	$destFilePath = $packagerPath, "/", $destFile -join ""
	$srcPath = "Files/", $sourceFile -join ""
	Write-Host "Copying:  $destFilePath"
	Copy-Item -Path $srcPath -Destination $destFilePath -Force
}

#
# Open the directory selectio nwindow, if requested
#
if ($customReportLoc -eq "Y" -or $customReportLoc -eq "y") {
	Write-Host " "
	Write-Host " "
	Write-Host "Opening directory selection window..."
	Write-Host " "
	Write-Host " "


	$folderBrowser = New-Object System.Windows.Forms.FolderBrowserDialog
	$folderBrowser.Description = "Select folder to save the generated Bug Reports (a new folder called KSP2_BugPackagerReports will be created)"
	$folderBrowser.SelectedPath = [Environment]::GetFolderPath('UserProfile')

	#
	# Check result from dialog selection widow
	#
	if ($folderBrowser.ShowDialog() -eq 'OK') {
	    $selectedFolder = $folderBrowser.SelectedPath
	    if ($folderBrowser.SelectedPath.Contains("$reportDir"))
	    {
		    #Write-Host "Selected report folder: $selectedFolder"
		    $directoryPath = $selectedFolder
	    } else {
			CreateReportDir -SelectedPath $selectedFolder
		    $directoryPath = $selectedFolder, "\", "$reportDir" -join ""
	    }
	} else {
	    Write-Host "No folder selected."
	    Start-Sleep -Seconds 5
	    exit
	}
} else
{
	CreateReportDir -SelectedPath $defaultReportLocation
    $directoryPath = $defaultReportLocation
}
Write-Host "Selected report folder: $directoryPath"

#
# Write the INI file data here
#
$iniFilePath = $packagerPath, "\", "KSP2_BugPackager.ini" -join ""

Set-Content -Path $iniFilePath -Value "[KSP2_BugPackager]"
Add-Content -Path $iniFilePath -Value "debug=1"
Add-Content -Path $iniFilePath -Value "zipFilePath=$directoryPath"
Add-Content -Path $iniFilePath -Value "pathToGameDirectory=$path"

#
# Create a shortcut on the desktop
#
$iconPath = $packagerPath, "\", "KSP2_BugPackager.ico" -join ""
$targetScriptPath = $packagerPath, "\", "KSP2_BugPackager.ps1" -join ""
$shortcutName = "KSP2 Bug Packager"

$desktopPath = [Environment]::GetFolderPath("Desktop")
$shortcutPath = Join-Path -Path $desktopPath -ChildPath "$shortcutName.lnk"

$WshShell = New-Object -ComObject WScript.Shell
$shortcut = $WshShell.CreateShortcut($shortcutPath)
$shortcut.TargetPath = "powershell.exe"
$shortcut.Arguments = "-ExecutionPolicy Bypass -File `"$targetScriptPath`""
$shortcut.IconLocation = $iconPath
$shortcut.Save()

Write-Host "Shortcut created on the desktop: $shortcutPath"


Write-Host " "
Write-Host "Installation completed"
Start-Sleep 1

#
# Closing tasks
#
Write-Host " "
Write-Host " "
Write-Host " "
$yn = Read-Host -Prompt "Do you want to run the KSP2 Bug Packager now (enter Y for yes)? "
if ($yn -ne "Y" -and $yn -ne "y") {
	Write-Host " "
	Write-Host "Installation completed" #, opening install/game folder"
	#Start-Sleep 5
	#Invoke-Item -Path $path
	Start-Sleep 2
	Write-Host "Exiting..."
	Start-Sleep -Seconds 2
	exit
}

# Change to the desired directory
Set-Location -Path $path

# Run the script
& "$targetScriptPath"

