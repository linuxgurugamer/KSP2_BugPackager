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

============
Installation
============

Unpack the zip file into a folder
Double-click on the install.bat file


=============================================
Technical Information
=============================================

While you should never need to change it, the following is provided for those people who would 
want to manually customize the config

======================
INI file Documentation
======================
                                                        
zipFilePath                 This contains the full path to where you want the script to saved   
                            the zip file

pathToGameDirectory         Replace with the path to the directory where KSP 2 is.




=====
Usage
=====
Once the INI file is configured, you can start the script by double-clicking on 
the KSP2_PowerShell.bat file.  A window will open up with entry fields for the following:


Enter Bug title:        
Please enter the bug description:

There will also be a second window where you can drag and drop files which you want to include with the report


Fill out the title and description.  Keep the title short, with no special characters, this will be used for the name of the zip file

After filling out the title and description, new listbox will be added with all the campaigns available.  Select the campaign which illustrates the bug, then click the "Select Campaign" button

After selecting the campaign, a list of all the saves in that campaign will be displayed.  Select a save and click the "Select Save" button

At this point, if you want to include  a workspace, click the checkbox and select a workspace following the same procedure



When you are done entering information click the button labeled "Finalize Bug Report".  The data will be packaged up into a zip file, and the folder where it is will be opened.  

The final step is to upload the report.  The have specified two different places to upload bug reports, there are two buttons at the lower-right of the window, one for each.  Click the button you want to use, the script will open up the appropriate page. 

