
@echo off

set version=""
FOR /F "tokens=* delims=" %%x in (version.txt) DO set version=%%x


copy Code\KSP2_BugPackager.bat Release
copy Code\KSP2_BugPackager.ini-example Release\KSP2_BugPackager.ini-example
copy Code\KSP2_BugPackager.ps1 Release
copy README.md Release
copy Changelog.txt Release\KSP_BugPackager-Changelog.txt

zip -9r KSP2_BugPackager-%version%.zip Release
