#
# Written by ShadowZone
# Modified by Linuxgurugamer
#
# This script collects the current .log files and packages them into a .zip file to send off to the developers.
# It also asks the user which save file to package into a second .zip file.
# Optional: Users can add a workspace file if the error is specific to a certain vehicle they created.

# Copyright (C) 2023  Linuxgurugamer & ShadowZone

 
# Specify the path to the INI file
$iniPath = ".\KSP2_BugPackager.ini"

# Define a function to parse the INI file
function Get-IniContent ($path) {
    $ini = @{}
    switch -regex -file $path {
        "^\[(.+)\]$" {
            $section = $matches[1]
            $ini[$section] = @{}
        }
        "^\s*([^#].+?)\s*=\s*(.+)$" {
            $name,$value = $matches[1..2]
            $ini[$section][$name] = $value
        }
    }
    return $ini
}

function Test-NumericRange {
    param (
        [Parameter(Mandatory=$true)]
        [AllowEmptyString()]
        [string]$Variable,
        
        [Parameter(Mandatory=$true)]
        [ValidateNotNullOrEmpty()]
        [int]$MinValue,
        
        [Parameter(Mandatory=$true)]
        [ValidateNotNullOrEmpty()]
        [int]$MaxValue
    )
    
    if ([int]::TryParse($Variable, [ref]$null)) {
        $NumericValue = [int]$Variable
        if ($NumericValue -ge $MinValue -and $NumericValue -le $MaxValue) {
            return $true
        }
        Write-Host "Please enter a number in the correct range"
        return $false
    }
    Write-Host "Please enter a valid number"
    return $false
}

##########################################

function GetOptionalFiles {

    Add-Type -AssemblyName System.Windows.Forms

    # Create a new form object
    $form = New-Object System.Windows.Forms.Form

    # Set the form properties
    $form.Text = "Drag and Drop Window"
    $form.FormBorderStyle = "FixedDialog"
    $form.MaximizeBox = $false
    $form.StartPosition = "CenterScreen"

    # Set the form size
    $form.Width = 405
    $form.Height = 435

    # Allow files to be dropped onto the form
    $form.AllowDrop = $true

    # Add a label to the form
    $label = New-Object System.Windows.Forms.Label
    $label.Location = New-Object System.Drawing.Point(10, 10)
    $label.Text = "Drag and drop files onto this window."
    $form.Controls.Add($label)

    # Add a list box to the form to display dropped files
    $listBox = New-Object System.Windows.Forms.ListBox
    $listBox.Location = New-Object System.Drawing.Point(10, 40)
    $listBox.Size = New-Object System.Drawing.Size(380, 300)
    $form.Controls.Add($listBox)

    # Add a close button to the form
    $button = New-Object System.Windows.Forms.Button
    $button.Location = New-Object System.Drawing.Point(150, 360)
    $button.Size = New-Object System.Drawing.Size(100, 30)
    $button.Text = "Close & Finish"
    $form.AcceptButton = $button
    $form.Controls.Add($button)

    # Add an event handler for the drag and drop event
    $form.add_DragEnter({
        # Check if any files are being dragged onto the form
        if ($_.Data.GetDataPresent([System.Windows.Forms.DataFormats]::FileDrop)) {
            $_.Effect = [System.Windows.Forms.DragDropEffects]::Copy
        }
    })

    $form.add_DragDrop({
        # Get the list of dropped files and display them in the list box
        $files = $_.Data.GetData([System.Windows.Forms.DataFormats]::FileDrop)
        foreach ($file in $files) {
            $listBox.Items.Add($file)
        }
    })

    # Add an event handler for the close button
    $button.add_Click({
        # Output the list of dropped files to the console
        New-Object -TypeName System.Collections.ArrayList
        ## Close the form
        $form.DialogResult = [System.Windows.Forms.DialogResult]::OK
        $form.Close()
    })

    # Show the form
    $result = $form.ShowDialog()
    if ($result -eq [System.Windows.Forms.DialogResult]::OK) {
        $form.Dispose()

                $files = @()
        foreach ($file in $listBox.Items) {
            #Write-Host $file
            $files += $file
        }
        # Close the form
        $form.DialogResult = [System.Windows.Forms.DialogResult]::OK
        $form.Close()
        return $files

    }


}


# Call the function to parse the INI file
$config = Get-IniContent $iniPath

# Access the values in the INI file
$debug = $config["KSP2_BugPackager"]["debug"]
$allInOneFile= $config["KSP2_BugPackager"]["allInOneFile"]
$zipFilePath = $config["KSP2_BugPackager"]["zipFilePath"]
$pathToGameDirectory = $config["KSP2_BugPackager"]["pathToGameDirectory"]

$pathToCampaignDirectories="$env:APPDATA\..\LocalLow\Intercept Games\Kerbal Space Program 2\Saves\SinglePlayer"



if ($debug -gt "0") {
    # Display the values
    Write-Host "debug: $debug"
    Write-Host "allInOneFile: $allInOneFile"
    Write-Host "zipFilePath: $zipFilePath"
    Write-Host "pathToGameDirectory: $pathToGameDirectory"
}
if ($debug -gt "1") {
    Set-PSDebug -Trace 2
    Write-Host "Debugging set to Trace 2"
}

Write-Host "----------------------------------------------------------------------------------------"
Write-Host "----------------------------------------------------------------------------------------"
Write-Host ""
Write-Host "     KSP2 Bug Report Assist Script by ShadowZone & Linuxgurugamer"
Write-Host ""
Write-Host "----------------------------------------------------------------------------------------"
Write-Host "----------------------------------------------------------------------------------------"

# Set the path to the folder where you want to save the zip file
$zipPath = $zipFilePath

$goodFile=0
Do {
    # Prompt the user to enter a name for the zip file
    $bugTitle = Read-Host "Enter Bug title"

    $zipLogFiles = $bugTitle + "_logs"
    $zipLogTmp = Join-Path $zipPath $zipLogFiles
    $zipLogPath = $zipLogTmp + ".zip"
    
    if (Test-Path $zipLogPath) {
        Write-Host ""
        Write-Host "The file: $zipLogPath  exists, please try again"
        Write-Host ""
    } else {
        $goodFile = 1
    }

} Until ($goodFile -eq 1)

if ($allInOneFile -eq "true") {
    $zipSaveFiles = $zipLogFiles
    $zipSaveTmp = $zipLogTmp
    $zipSavePath = $zipLogPath
} else {
    $zipSaveFiles = $bugTitle + "_savefile"
    $zipSaveTmp = Join-Path $zipPath $zipSaveFiles
    $zipSavePath = $zipSaveTmp + ".zip"
}

Write-Host "----------------------------------------------------------------------------------------"
Write-Host ""
Write-Host "Please enter the bug description.  Enter a blank line when you're finished:"
$multilineText = ""
while ($line = [console]::readline()) {
    $multilineText += $line + "`n"
}
$multilineText = $multilineText.Trim()

$bugDescrFilePath="BugDescription.txt"
Set-Content -Path $bugDescrFilePath -Value $multilineText


# Set the paths to the files you want to collect
$file1Path="$env:APPDATA\..\LocalLow\Intercept Games\Kerbal Space Program 2\Player.log"
$file2Path = "$pathToGameDirectory\Ksp2.log"

# Create the .zip file containing the logs
Compress-Archive -Path $file1Path, $file2Path, $bugDescrFilePath -DestinationPath $zipLogPath
Remove-Item -Path $bugDescrFilePath -Force
Write-Host "Logs packaged into $zipLogPath.zip"
Write-Host "----------------------------------------------------------------------------------------"
Write-Host ""


$campaignFolderPath = $pathToCampaignDirectories
# Prompt the user to enter a directory path
$dir = $campaignFolderPath

# Get a list of all directories in the specified directory
$directories = Get-ChildItem $dir | Where-Object {$_.PSIsContainer}

# Display a numbered list of the directories
for ($i = 0; $i -lt $directories.Count; $i++) {
    Write-Host ("{0}. {1}" -f ($i+1), $directories[$i].Name)
}
Write-Host ""

Do {
    # Prompt the user to select a directory
    $selection = Read-Host "Enter the number of the directory to select"
} Until (Test-NumericRange -Variable $selection -Minvalue 1 -MaxValue $directories.Count)

# Validate the user's selection
if ([int]$selection -ge 1 -and [int]$selection -le $directories.Count) {
    $selectedDirectory = $directories[$selection-1].FullName
    Write-Host ""
    Write-Host "You selected $selectedDirectory"
} else {
    Write-Host "Invalid selection"
}

Write-Host "----------------------------------------------------------------------------------------"
Write-Host ""

# Set the path to the folder containing the save files"
$saveFolderPath = $selectedDirectory

# Get the list of save files in the folder, sorted by last modified date
$saveFiles = Get-ChildItem $saveFolderPath -Filter "*.json" | Sort-Object LastWriteTime -Descending

# Display the list of save files to the user
Write-Host "Select a save file to package into the second zip file"
for ($i = 0; $i -lt $saveFiles.Count; $i++) {
    $fileNameWithoutExtension = [System.IO.Path]::GetFileNameWithoutExtension($saveFiles[$i].FullName)
    Write-Host "$($i + 1). $fileNameWithoutExtension"
}

# Prompt the user to enter the number corresponding to the selected file
Write-Host ""

$goodIndex=0
Do {
    $saveFileIndex = Read-Host "Enter the number of the file you want to include"
} Until (Test-NumericRange -Variable $saveFileIndex -Minvalue 1 -MaxValue $saveFiles.Count)
    
# Get the path of the selected save file without the .json extension
$saveFilePath = [System.IO.Path]::ChangeExtension($saveFiles[$saveFileIndex - 1].FullName, $null)

# Generate variables to also package .meta and .jpg files and put them into an array
$saveFileJson = $saveFilePath + "json"
$saveFileMeta = $saveFilePath + "meta"
$saveFileJpg = $saveFilePath + "jpg"
$saveArray = @($saveFileJson, $saveFileMeta, $saveFileJpg)


# Set the path to the folder containing the workspace files
$workspacePath = Join-Path $saveFolderPath "Workspaces"


# Prompt the user if they want to include a workspace
Write-Host "----------------------------------------------------------------------------------------"
Write-Host ""
$includeWorkspace = Read-Host "Do you want to include a workspace? (y/N)"
Write-Host ""
if ($includeWorkspace -eq "y") {
    # Get a list of workspace files and display them to the user
    $workspaceFiles = Get-ChildItem -Path $workspacePath -Filter *.json | Sort-Object -Property LastWriteTime -Descending
	Write-Host ""
    Write-Host "Select a Workspace to include alongside the save file from the list:"
	Write-Host ""
    for ($i = 0; $i -lt $workspaceFiles.Count; $i++) {
        $workspaceFile = $workspaceFiles[$i].Name.Replace(".json", "")
        Write-Host "$($i+1). $workspaceFile"
    }
    Do {
        # Prompt user to select workspace by entering corresponding number
        Write-Host ""
        $workspaceIndex = Read-Host "Enter the number of the workspace you want to include"
    } Until (Test-NumericRange -Variable $workspaceIndex -Minvalue 1 -MaxValue $workspaceFiles.Count)

    if ($workspaceIndex -ne "") {
        $workspaceFilePath = [System.IO.Path]::ChangeExtension($workspaceFiles[$workspaceIndex - 1].FullName, $null)

		# Get full paths and also just the file name of the workspace files. Just file names are necessary for creating the entry in the .zip file later
		$workspaceJson = $workspaceFilePath + "json"
		$workspaceJsonName = Split-Path -Path $workspaceJson -Leaf
		$workspaceMeta = $workspaceFilePath + "meta"
		$workspaceMetaName = Split-Path -Path $workspaceMeta -Leaf
		$workspaceJpg = $workspaceFilePath + "jpg"
		$workspaceJpgName = Split-Path -Path $workspaceJpg -Leaf
	
		# Create .zip file with save files
        if ($allInOneFile -eq "true") {
            Compress-Archive -Path $saveArray -Update -DestinationPath $zipSavePath
        } else {
            Compress-Archive -Path $saveArray -DestinationPath $zipSavePath
        }
		$zip = [System.IO.Compression.ZipFile]::Open($zipSavePath, 'Update')
	
		# Create subfolder "Workspaces" inside .zip file
		$zip.CreateEntry("Workspaces/")

		# Add workspace files into subfolder inside .zip.file
		$compression = [System.IO.Compression.CompressionLevel]::Fastest
		[System.IO.Compression.ZipFileExtensions]::CreateEntryFromFile($zip,$workspaceJson, "Workspaces\$workspaceJsonName",$compression)
		[System.IO.Compression.ZipFileExtensions]::CreateEntryFromFile($zip,$workspaceMeta, "Workspaces\$workspaceMetaName",$compression)
		[System.IO.Compression.ZipFileExtensions]::CreateEntryFromFile($zip,$workspaceJpg, "Workspaces\$workspaceJpgName",$compression)
		$zip.Dispose()
    } else {
     # No workspace specified, just package save file data.
       Compress-Archive -Path $saveArray -Update  -DestinationPath $zipSavePath
	}
} else {
    # If user does not want to include workspace, just package save file data.
	Compress-Archive -Path $saveArray -Update  -DestinationPath $zipSavePath
}

$f = GetOptionalFiles 
if ($f.Count -gt 0) {
    Write-Host "Adding files to zip file"
	$zip = [System.IO.Compression.ZipFile]::Open($zipSavePath, 'Update')
	
	# Create subfolder "Files" inside .zip file
	$zip.CreateEntry("Files/")
	$compression = [System.IO.Compression.CompressionLevel]::Fastest
    foreach ($f1 in $f) {

		$name = (Get-Item $PSCommandPath ).Name 
		[System.IO.Compression.ZipFileExtensions]::CreateEntryFromFile($zip, $f, "Files\$name",$compression)
    }
    $zip.Dispose()

}


Write-Host ""
Write-Host "----------------------------------------------------------------------------------------"
Write-Host "----------------------------------------------------------------------------------------"
Write-Host ""
Write-Host "Bug report zip files are completed, stored in: $zipFilePath"

if ($allInOneFile -eq "true") {
    Write-Host ""
    Write-Host "All files are in the zip file:  $zipLogPath"
} else {
    Write-Host "Files are stored in the following two zip files:"
    Write-Host ""
    Write-Host $zipLogPath
    Write-Host $zipSavePath
}

Write-Host ""
Write-Host ""

Read-Host "Done, press <ENTER> to continue"
