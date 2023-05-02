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
icon_file = "no-kraken-icon-64.png"
if os.path.isfile(icon_file):
    root.call("wm", "iconphoto", root._w, PhotoImage(file=icon_file))  # this worked, although the image quality could be better
# icon = PhotoImage(file="no-kraken-icon.png")
# root.iconphoto(False, icon)

# Setup main form frame withing window
form = ttk.Frame(root, padding=10)
form.pack(padx=1, pady=1, expand=True, fill="both")

# main_frame = Frame(form)

# Header Group
header_group_frame = Frame(form)
header_group_frame.pack(padx=1, pady=1, side="top", anchor="nw", expand=True, fill="x")

# Title
title_frame = Frame(header_group_frame)
title_frame.pack(padx=1, pady=1, side="top", anchor="nw", expand=True, fill="x")
title_label = Label(title_frame, text = "Enter Bug Title:")
title_label.pack(padx=1, pady=1, side="top", anchor="w")
title_entry = Entry(title_frame)
title_entry.pack(padx=1, pady=1, side="top", anchor="w", expand=True, fill="x")

# Title
description_frame = Frame(header_group_frame)
description_frame.pack(padx=1, pady=1, side="top", anchor="nw", expand=True, fill="x")
description_label = Label(description_frame, text = "Please enter the bug description:")
description_label.pack(padx=1, pady=1, side="top", anchor="w")
description_entry = Entry(description_frame, justify="left")
description_entry.pack(padx=1, pady=1, side="top", anchor="w", expand=True, fill="x")

# First Group
first_group_frame = Frame(form)
first_group_frame.pack(padx=1, pady=1, side="top", expand=True, fill="both")

# Campaign
campaign_frame = Frame(first_group_frame)
campaign_frame.pack(padx=1, pady=1, side="left", anchor="nw", expand=True, fill="both")
campaign_label = Label(campaign_frame ,text = "Select the campaign\n(sorted alphabetically)", justify="left")
campaign_label.pack(padx=1, pady=1, side="top", anchor="w")
campaign_list = Listbox(campaign_frame, exportselection=False)
campaign_list.pack(padx=1, pady=1, side="left", expand=True, fill="both")
campaign_list_scrollbar = Scrollbar(campaign_frame, orient="vertical")
campaign_list.config(yscrollcommand=campaign_list_scrollbar.set)
campaign_list_scrollbar.config(command=campaign_list.yview)
campaign_list_scrollbar.pack(pady=2, side="left", fill="y")
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
save_frame = Frame(first_group_frame)
save_frame.pack(padx=1, pady=1, side="left", expand=True, fill="both", anchor="n")
save_label = Label(save_frame ,text = "Select the Save\n(newest first)", justify="left")
save_label.pack(padx=1, pady=1, side="top", anchor="w")
save_list = Listbox(save_frame, exportselection=False, )
save_list.pack(padx=1, pady=1, side="left", expand=True, fill="both")
save_list_scrollbar = Scrollbar(save_frame, orient="vertical")
save_list.config(yscrollcommand=save_list_scrollbar.set)
save_list_scrollbar.config(command=save_list.yview)
save_list_scrollbar.pack(pady=2, side="left", fill="y")

# Workspace
workspace_frame = Frame(first_group_frame)
workspace_frame.pack(padx=1, pady=1, side="left", expand=True, fill="both", anchor="n")
workspace_label = Label(workspace_frame ,text = "Select the workspace\n(newest first)", justify="left")
workspace_label.pack(padx=1, pady=1, side="top", anchor="w")
include_workspace = IntVar()
def workspace_checkbox_handler():
    print_debug(include_workspace.get())
workspace_checkbox = Checkbutton(workspace_frame, text="Include a workspace", variable=include_workspace, command=workspace_checkbox_handler)
workspace_checkbox.pack(padx=1, pady=1, side="top", anchor="w")
workspace_list = Listbox(workspace_frame, exportselection=False)
workspace_list.pack(padx=1, pady=1, side="left", expand=True, fill="both")
workspace_list_scrollbar = Scrollbar(workspace_frame, orient="vertical")
workspace_list.config(yscrollcommand=workspace_list_scrollbar.set)
workspace_list_scrollbar.config(command=workspace_list.yview)
workspace_list_scrollbar.pack(pady=2, side="left", fill="y")

# Files
files_frame = Frame(form)
files_frame.pack(padx=1, pady=1, side="top", expand=True, fill="both")
files_buttons_frame = Frame(files_frame)
files_buttons_frame.pack(padx=1, pady=1, side="bottom", anchor="w")
def add_files_handler():
    for file in filedialog.askopenfilenames():
        files_list.insert(0,file)
def remove_files_handler():
    files_list.delete(files_list.curselection()[0])
def clear_files_handler():
    files_list.delete(0,'end')
ttk.Button(files_buttons_frame, text="Add file(s)...", command=add_files_handler).pack(padx=1, pady=1, side="left")
ttk.Button(files_buttons_frame, text="Remove file(s)...", command=remove_files_handler).pack(padx=1, pady=1, side="left")
ttk.Button(files_buttons_frame, text="Clear file(s)...", command=clear_files_handler).pack(padx=1, pady=1, side="left")
files_label = Label(files_frame ,text = "Files:", justify="left")
files_label.pack(padx=1, pady=1, side="top", anchor="w")
files_list = Listbox(files_frame)
files_list.pack(padx=1, pady=1, side="left", expand=True, fill="both")
files_list_scrollbar = Scrollbar(files_frame, orient="vertical")
files_list.config(yscrollcommand=files_list_scrollbar.set)
files_list_scrollbar.config(command=files_list.yview)
files_list_scrollbar.pack(pady=2, side="left", fill="y")

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
footer_frame = Frame(form)
footer_frame.pack(padx=1, pady=1, side="top", anchor="w")
ttk.Button(footer_frame, text="Generate Bug Report", command=package_bug_report).pack(padx=1, pady=1, side="top")

# Links
def callback(url):
   webbrowser.open_new_tab(url)
link1 = Label(footer_frame, text="Private Division Customer Support",font=('Helveticabold', 12), fg="blue", cursor="hand2")
link1.pack(padx=1, pady=1, side="top")
link1.bind("<Button-1>", lambda e: callback("https://support.privatedivision.com/hc/en-us/requests/new?ticket_form_id=360001675633"))
link2 = Label(footer_frame, text="Dedicated Bug Reports on the KSP Subforum",font=('Helveticabold', 12), fg="blue", cursor="hand2")
link2.pack(padx=1, pady=1, side="top")
link2.bind("<Button-1>", lambda e: callback("https://forum.kerbalspaceprogram.com/index.php?/forum/144-ksp2-bug-reports/"))

form.mainloop()
