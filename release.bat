
@echo off

set version=""
FOR /F "tokens=* delims=" %%x in (Version.txt) DO set version=%%x


copy Code\KSP2_BugPackager.bat Release\Files\KSP2_BugPackater.bat-dist
copy Code\KSP2_BugPackager.ini-example Release\Files\KSP2_BugPackager.ini-example
copy Code\KSP2_BugPackager.ps1 Release\Files\KSP2_BugPackager.ps1-dist
copy Code\install.bat Release
copy Code\install.ps1 Release\Files
copy README.md Release
copy Credits.txt Release
copy Changelog.txt Release\KSP_BugPackager-Changelog.txt

zip -9r KSP2_BugPackager-%version%.zip Release
