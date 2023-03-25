#!/usr/bin/env python3

import os
import re
import configparser
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import webbrowser
import zipfile
import textwrap
from datetime import datetime, timezone

# Specify the path to the INI file
INI_PATH = "KSP2_BugPackager.ini"
KSP2_STEAM_APP_ID = "954850"

# Check if file doesn't exists
if not os.path.isfile(INI_PATH):
    print("The INI file: {} does not exist.  Attempting to use sane defaults.".format(INI_PATH))
    exit

# Parse the INI file
config = configparser.ConfigParser()
config.read(INI_PATH)

# Access the values in the INI file
if "KSP2_BugPackager" not in config:
    config["KSP2_BugPackager"] = {}
debug = config["KSP2_BugPackager"].setdefault("debug", "1")
zipFilePath = config["KSP2_BugPackager"].setdefault("zipFilePath", "/tmp")
pathToGameDirectory = config["KSP2_BugPackager"].setdefault("pathToGameDirectory", os.path.expanduser('~') + "/.local/share/Steam/steamapps/compatdata/" + KSP2_STEAM_APP_ID + "/pfx/drive_c/users/steamuser/AppData/LocalLow/Intercept Games/Kerbal Space Program 2")
pathToCampaignDirectories = config["KSP2_BugPackager"].setdefault("pathToCampaignDirectories", config["KSP2_BugPackager"]["pathToGameDirectory"] + "/Saves/SinglePlayer")

def print_debug(thing):
    if debug == "1": print(thing)

print_debug("debug: {}".format(debug))
print_debug("zipFilePath: {}".format(zipFilePath))
print_debug("pathToGameDirectory: {}".format(pathToGameDirectory))
print_debug("pathToCampaignDirectories: {}".format(pathToCampaignDirectories))

# Setup root window
root = Tk()
root.title("KSP2 Debug Reporter")

# Setup main form frame withing window
form = ttk.Frame(root, padding=10)
form.grid()

# Title
title_label = Label(form, text = "Enter Bug Title:")
title_label.grid(row = 0,column = 0, sticky="E")
title_entry = Entry(form, width=50)
title_entry.grid(row = 0,column = 1, sticky="W")

# Description
description_label = Label(form ,text = "Please enter the bug description:")
description_label.grid(row = 1,column = 0, sticky="E")
description_entry = Entry(form, width=50, justify="left")
description_entry.grid(row = 1,column = 1, sticky="W")

# Campaign
campaign_label = Label(form ,text = "Select the campaign\n(sorted alphabetically)")
campaign_label.grid(row = 3,column = 0, sticky="E")
campaign_list = Listbox(form, exportselection=False, width=100)
campaign_list.grid(row = 3,column = 1)
campaign_list_scrollbar = Scrollbar(form, orient="vertical")
campaign_list.config(yscrollcommand=campaign_list_scrollbar.set)
campaign_list_scrollbar.config(command=campaign_list.yview)
campaign_list_scrollbar.grid(row=3,column=3, sticky="ns")
dirs = os.listdir(pathToCampaignDirectories)
dirs.sort(reverse=True)
for dir in dirs:
    campaign_list.insert(0, dir)
def campaign_list_click_handler(event):
    save_list.delete(0,'end')
    dir_listing = os.listdir(pathToCampaignDirectories + "/" + campaign_list.get(campaign_list.curselection()[0]))
    json_files_re = re.compile(".*\.json")
    dir_listing = [ i for i in dir_listing if json_files_re.match(i) ]
    dir_listing.sort(reverse=True)
    for item in dir_listing:
        item_stripped = re.sub(r'\..*$', '', item)
        save_list.insert(0, item_stripped)
    workspace_list.delete(0,'end')
    dir_listing = os.listdir(pathToCampaignDirectories + "/" + campaign_list.get(campaign_list.curselection()[0]) + "/Workspaces")
    json_files_re = re.compile(".*\.json")
    dir_listing = [ i for i in dir_listing if json_files_re.match(i) ]
    dir_listing.sort(reverse=True)
    for item in dir_listing:
        item_stripped = re.sub(r'\..*$', '', item)
        workspace_list.insert(0, item_stripped)
campaign_list.bind("<ButtonRelease>",campaign_list_click_handler)
campaign_list.bind("<KeyRelease>",campaign_list_click_handler)

# Save
save_label = Label(form ,text = "Select the Save\n(newest first)")
save_label.grid(row = 4,column = 0, sticky="E")
save_list = Listbox(form, exportselection=False, width=100, )
save_list.grid(row = 4,column = 1)
save_list_scrollbar = Scrollbar(form, orient="vertical")
save_list.config(yscrollcommand=save_list_scrollbar.set)
save_list_scrollbar.config(command=save_list.yview)
save_list_scrollbar.grid(row=4,column=3, sticky="ns")

# Workspace
include_workspace = IntVar()
def workspace_checkbox_handler():
    print_debug(include_workspace.get())
workspace_checkbox = Checkbutton(form, text="Include a workspace", variable=include_workspace, command=workspace_checkbox_handler)
workspace_checkbox.grid(row = 5,column = 0)
workspace_label = Label(form ,text = "Select the workspace\n(newest first)")
workspace_label.grid(row = 6,column = 0, sticky="E")
workspace_list = Listbox(form, exportselection=False, width=100)
workspace_list.grid(row = 6,column = 1)
workspace_list_scrollbar = Scrollbar(form, orient="vertical")
workspace_list.config(yscrollcommand=workspace_list_scrollbar.set)
workspace_list_scrollbar.config(command=workspace_list.yview)
workspace_list_scrollbar.grid(row=6,column=3, sticky="ns")

# Files
files_label = Label(form ,text = "Files:")
files_label.grid(row = 7,column = 0, sticky="E")
files_list = Listbox(form, width=100)
files_list.grid(row = 7,column = 1)
files_list_scrollbar = Scrollbar(form, orient="vertical")
files_list.config(yscrollcommand=files_list_scrollbar.set)
files_list_scrollbar.config(command=files_list.yview)
files_list_scrollbar.grid(row=7,column=3, sticky="ns")
def add_files_handler():
    for file in filedialog.askopenfilenames():
        files_list.insert(0,file)
def remove_files_handler():
    files_list.delete(files_list.curselection()[0])
def clear_files_handler():
    files_list.delete(0,'end')
files_buttons_frame = Frame(form)
files_buttons_frame.grid(row=8,column=1)
ttk.Button(files_buttons_frame, text="Add file(s)...", command=add_files_handler).pack(side="left")
ttk.Button(files_buttons_frame, text="Remove file(s)...", command=remove_files_handler).pack(side="left")
ttk.Button(files_buttons_frame, text="Clear file(s)...", command=clear_files_handler).pack(side="left")

# Links
def callback(url):
   webbrowser.open_new_tab(url)
link1 = Label(form, text="Private Division Customer Support",font=('Helveticabold', 15), fg="blue", cursor="hand2")
link1.grid(row=12, column=0)
link1.bind("<Button-1>", lambda e: callback("https://support.privatedivision.com/hc/en-us/requests/new?ticket_form_id=360001675633"))
link2 = Label(form, text="Dedicated Bug Reports on the KSP Subforum",font=('Helveticabold', 15), fg="blue", cursor="hand2")
link2.grid(row=13, column=0)
link2.bind("<Button-1>", lambda e: callback("https://forum.kerbalspaceprogram.com/index.php?/forum/144-ksp2-bug-reports/"))

# Report
def package_bug_report():

    bugTitle = title_entry.get()
    bugDescr = description_entry.get()
    
    selectedCampaign = campaign_list.get(campaign_list.curselection()[0])
    selectedCampaignIndex = campaign_list.curselection()[0]
    
    selectedSave = save_list.get(save_list.curselection()[0])
    selectedSaveIndex = save_list.curselection()[0]
    
    zipLogFiles = bugTitle + "_logs_" + datetime.now(timezone.utc).strftime("%Y-%m-%d_%H-%M-%S")
    zipLogTmp = zipFilePath + "/" + zipLogFiles
    zipSavePath = zipLogTmp + ".zip"
    
    print_debug("Bug title: {}".format(bugTitle))
    print_debug("Bug Descr: {}".format(bugDescr))
    print_debug("Selected Campaign: {}".format(selectedCampaign))
    print_debug("Save: {}".format(selectedSave))
        
	# Initializing zip file names
    zipSaveFiles = zipLogFiles
    zipSaveTmp = zipLogTmp
    print_debug("zipSaveFiles: {}".format(zipSaveFiles))
    print_debug("zipSaveTmp: {}".format(zipSaveTmp))
    print_debug("zipSavePath: {}".format(zipSavePath))

    bugDescrFilePath="BugDescription.txt"
    bug_description_file_contents = textwrap.dedent("""\
        Bug report packaged by KSP2_BugPackager.py

        """ + bugDescr + """
        """)

	# Set the paths to the files you want to collect
    player_log_path = pathToGameDirectory + "/Player.log"  # file1Path
    player_log_path_contents = open(player_log_path, "r").read()
    ksp2_log_path = os.path.expanduser('~') + "/.steam/steam/steamapps/common/Kerbal Space Program 2/Ksp2.log"  # file2Path
    ksp2_log_path_contents = open(ksp2_log_path, "r").read()
    
    print_debug("Creating zip file: {}".format(zipSavePath))
    print_debug("Adding player_log_path to zip file: {}".format(player_log_path))
    print_debug("Adding ksp2_log_path to zip file: {}".format(ksp2_log_path))
    print_debug("Adding bugDescrFilePath to zip file: {}".format(bugDescrFilePath))

    print_debug("selectedSaveIndex: {}".format(selectedSaveIndex))

    saveFilePath = pathToCampaignDirectories + "/" + campaign_list.get(campaign_list.curselection()[0]) + "/"
    save_file_base_name = save_list.get(save_list.curselection()[0])
    
    saveFileJson = saveFilePath + save_file_base_name + ".json"
    saveFileMeta = saveFilePath + save_file_base_name + ".meta"
    saveFileJpg = saveFilePath + save_file_base_name + ".jpg"
    saveFilePng = saveFilePath + save_file_base_name + ".png"
    saveList = []
    if os.path.isfile(saveFileJson): saveList += [ save_file_base_name + ".json" ]
    if os.path.isfile(saveFileMeta): saveList += [ save_file_base_name + ".meta" ]
    if os.path.isfile(saveFilePng): saveList += [ save_file_base_name + ".png" ]
    if os.path.isfile(saveFileJpg): saveList += [ save_file_base_name + ".jpg" ]
    print_debug("saveList: {}".format(saveList))


	##############################
	# Adding workspace to zip file
    print_debug("include_workspace: {}".format(include_workspace.get()))
    if include_workspace.get() == 1:
		# Get full paths and also just the file name of the workspace files. Just file names are necessary for creating the entry in the .zip file later
        workspace_directory = pathToCampaignDirectories + "/" + campaign_list.get(campaign_list.curselection()[0]) + "/Workspaces"
        workspace_file_list = []
        workspace_base_name = workspace_list.get(workspace_list.curselection()[0])
        workspaceJson = workspace_directory + "/" + workspace_base_name + ".json"
        workspaceMeta = workspace_directory  + "/" + workspace_base_name + ".meta"
        workspaceJpg = workspace_directory  + "/" + workspace_base_name + ".jpg"
        workspacePng = workspace_directory  + "/" + workspace_base_name + ".png"
        if os.path.isfile(workspaceJson): workspace_file_list += [ workspace_base_name + ".json" ]
        if os.path.isfile(workspaceMeta): workspace_file_list += [ workspace_base_name + ".meta" ]
        if os.path.isfile(workspacePng): workspace_file_list += [ workspace_base_name + ".png" ]
        if os.path.isfile(workspaceJpg): workspace_file_list += [ workspace_base_name + ".jpg" ]
        print_debug("workspaceList: {}".format(workspace_file_list))

    # Add additional files    
    additional_files_list = files_list.get(0,'end')
    additional_files_dict = {}
    for each_file in additional_files_list:
        each_file_name = os.path.basename(each_file)
        additional_files_dict[each_file_name] = each_file
    print_debug("File Dictionary: {}".format(additional_files_dict))
    print_debug("File Dictionary Length: {}".format(len(additional_files_dict)))

	# Build the zip file
    with zipfile.ZipFile(zipSavePath, 'w') as zip:
        zip.writestr("Player.log", player_log_path_contents)
        zip.writestr("Ksp2.log", ksp2_log_path_contents)
        zip.writestr(bugDescrFilePath, bug_description_file_contents)
        for each_save_file in saveList:
            save_file_contents = open(saveFilePath + each_save_file, "rb").read()
            zip.writestr(each_save_file, save_file_contents)
        if include_workspace.get() == 1:
            for each_workspace_file in workspace_file_list:
                workspace_file_contents = open(workspace_directory + "/" + each_workspace_file, "rb").read()
                zip.writestr("Workspaces/" + each_workspace_file, workspace_file_contents)
        if len(additional_files_dict) > 0:
            for each_additional_filename,each_additional_filepath in additional_files_dict.items():
                additional_file_content = open(each_additional_filepath, "rb").read()
                zip.writestr("Files/" + each_additional_filename, additional_file_content)

# Create a button that, when clicked, will cause a zip file to be emitted.
ttk.Button(form, text="Generate Bug Report", command=package_bug_report).grid(row=10,column=4)

form.mainloop()
