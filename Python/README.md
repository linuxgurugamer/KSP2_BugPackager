# KSP2_BugPackager.py

This edition of KSP2_BugPackager currently targets Linux as the supported OS.

## Assumptions

This script currently expects KSP2 to have been installed via Steam through it's built-in Proton compatability layer.

## Dependencies

This was created under Ubuntu 20.04.5 LTS with Python 3.10.7.  I tried to avoid using any modules that are not provided by the Python Standard Library.

## Setup

### Steam Installation

These steps could be different on different flavors of Linux.
1. Go to https://steampowered.com and click on the green "Install Steam" button at the top.
2. Click on the blue "Install Steam" button.
3. On my version of Ubuntu this downloaded a Debian package named steam_latest.deb.
4. I installed this using apt-get: `apt-get install ./steam_latest.deb`  *Note: The ./ is needed to get apt-get to look at the local file.*

### Python Environment

I used [pyenv](https://github.com/pyenv/pyenv) to install Python 3.10.7.

The script may need execute permissions granted before you will be able to run it.
`chmod +x KSP2_BugPackager.py`

## Using the script

I attempted to match the functionality of the original PowerShell edition.  The usage instructions for that should generally apply.

### Execution

The script should be run from the same directory it's located in: `./KSP2_BugPackager.py`