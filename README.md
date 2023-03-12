This script is designed to package up all the files necessary to report
a bug to the KSP 2 developers

The script consists of three files, an INI file, a PowerShell .ps1 file and a batch file.  The 
INI file contains a description for each parameter, full explanation is further down

============
What it does
============
The script will gather up all files necessary to report a bug.  You will be prompted
for some information, and the files will be compiled into a zip file and stored
in a file.  All settings are configurable in the INI file.

The result will be in two zip files, one containing the logs and the second containing the save 
file(s)

======================
INI file Documentation
======================
Copy the file KSP2_BugPackager.ini-example to KSP2_BugPackager.ini and then edit it using
the following documentation of the variables:

debug                       Controls debugging level. 0 means no debugging, 1 displays
                            the values read from the INI file, 2 turns on PowerShell tracing
                            
allInOneFile                If true, all files will be packaged up into a single file.  Otherwise
                            there will be one file for the logs and a second file for the save files
                            
zipFilePath                 This contains the full path to where you want the script to saved   
                            the zip file

userName                    Replace with your Windows user name

pathToGameDirectory         Replace with the path to the directory where KSP 2 is.  The followin
                            two lines are examples of two different locations where KSP 2 lives on 
                            my system:

    pathToGameDirectory=C:\Program Files (x86)\Steam\steamapps\common\Kerbal Space Program 2
    pathToGameDirectory=U:\SteamLibrary\steamapps\common\Kerbal Space Program 2

pathToCampaignDirectories   This is the path to the SinglePlayer directory where the games are saved.
                            The following line is an example of where my files are:

    pathToCampaignDirectories=C:\Users\Linuxgurugame\AppData\LocalLow\Intercept Games\Kerbal Space Program 2\Saves\SinglePlayer

=====
Usage
=====
Once the INI file is configured, you can start the script by double-clicking on 
the KSP2_PowerShell.bat file.  The following prompts are displayed:

Enter Bug title:        Enter the title of the bug.  Keep this short, it is used as the name
                        of the zip file.  Also, if there is an existing zip file by that name
                        you will be prompted to enter a different one.  It is also advisable 
                        not use spaces

Please enter the bug description.  Enter a blank line when you're finished:

A list of all the campaigns in the SinglePlayer directory is then displayed.  Select
the campaign which you are reporting the bug occurred in.

Then a list of the save files for that campaign are displayed.  Again, select the one
which contains the bug.

Do you want to include a workspace? (y/N):  Yes or no, pressing return (or anything other than
                                            a "y") will bypass the workspaces
                                            
If you did reply with a "y", you will then be presented with a list of workspaces
Select the workspace to include.

The files will then be packaged up, and the names of the file(s) which contain the
bug report will be displayed.  When done, press <ENTER> to end the script and close the window
