# whatsapp-analyse: Parse and Analyse WhatsApp Chats

## Table of Content

- [Description](#description)
- [Installation](#installation)
- [Extract Data](#extract-data)
- [Usage](#usage)
- [Limitations](#limitations)
- [Building](#building)
- [Features to be added and Known Bugs](#features-to-add--bugs-to-solve)
## Description

whatsapp-analyse is a command-line program, to analyse personal or group WhatsApp chats. It requires Python3 to work and will work in all major operating systems.  
It is written procedurally with Python, i.e, without any user-defined classes.

## INSTALLATION

### For Windows

1. Download the whatsapp-analyse.exe file from releases ([Latest](https://github.com/ayashrath/analyze-whatsapp-chat/releases/download/v1.1/whatsapp-analyser.exe))
2. Then paste the whatsapp-analyse.exe file into any folder in Windows path (To find the list type - `echo %PATH%` in command prompt) **except System32 folder**

### For macOS and Linux/GNU OSs

    sudo curl -L https://github.com/ayashrath/analyze-whatsapp-chat/releases/download/v1.1/whatsapp-analyser -o /usr/local/bin/whatsapp-analyser
    sudo chmod a+rx /usr/local/bin/whatsapp-analyser

If you don't want to use curl, you can use wget:

    sudo wget https://github.com/ayashrath/analyze-whatsapp-chat/releases/download/v1.1/whatsapp-analyser -O usr/local/bin/whatsapp-analyser
    sudo chmod a+rx usr/local/bin/whatsapp-analyser

## Extract Data

### Android

Please refer to the [WhatsApp FAQ Page](https://faq.whatsapp.com/1180414079177245) for information on how to extract data which needs to be analysed.

### iOS

1. Open the chat you want to get analysed
2. Click on the name of the person (or group name) which appears in the top after step 1
3. Scroll to the bottom to find a button for export
4. Use it to export the chat -> we don't need media to be included wih out export
5. The file you get will a .zip file, extract it and get the .txt file out of it - This file  is what we will be working on

## Usage

    usage: whatsapp_analyse.py [-h] [-n] [-t] [-ll] [-l] [-w {1,2,3}] path

    Tool to analyse a WhatsApp Chat. Please refer to https://github.com/ayashrath/analyse-whatsapp-chat#extract-data for information on the procedure to export chat on a mobile device.

    positional arguments:
      path                  path of exported text file of chat
    
    options:
      -h, --help            show this help message and exit
      -n, --notification    obtain data on non-user messages (specifically for group chats) that occur in group chat, like a group's icon was changed
      -t, --total           obtain data on the chat as a whole, in addition to data computed by default (case where no flag has been used)
      -ll, --list-link      obtain categorised data of links present in the chat
      -l, --length          obtain detailed results concerning the length of messages
      -w {1,2,3}, --word-list {1,2,3}
                            obtain the list of unique words used [1 for just the list, 2 for 1 + count, and 3 for 2 + sender name]

### The default output of the tool
![Showcase Default Output](./media/default-flag.gif)

## Limitations

- Required a mobile device, to export data
- It works only the data available by exporting data of chat from the mobile app, i.e., it will not work on the chat that has been cleared by the person exporting the chat
- It can't analyse data which may appear on your phone but not present in the exported txt file. For example - in the app we can see all the members present in the group, but here we can get list of all members who have their chat in the exported .txt file

## Building

### To make a single executable from project files

1. Open the build.py file located in tests directory.
2. Change the values of variables FILE_LST, MODULES_LST and BUILD_ON_UNIX_SYSTEM, if required.
3. Run the script, and you should get file - whatsapp-analyse-full.
4. If on macOS or Linux, to make them executable and use the shebang - `chmod +x whatsapp-analyse-full`.
5. For windows
    1. Install [PyInstaller](https://github.com/pyinstaller/pyinstaller).
    2. Clone this repository.
    3. Then type this in command prompt or Powershell - `pyinstaller --noconfirm --onefile --console --clean whatsapp-analyse-full`.
    4. Then the .exe file can be found in the dist folder in the directory where you ran the above command.

## Features to add / Bugs to solve

### Please do report any bugs you encounter, which is not in the list below:

- New flags, that are planned to be added
  - Poll data analysis - Shows details of polls that were present on the group
  - Graphical analysis - Gives graphical output of the analysis, on appropriate areas
  - Date and time analysis - Makes use of the date and time data available
  - Full analysis report return - Generates a full report in a single file, for sharing purposes
- Emoji count: Gives a count of emojis in default and total flags
- Better data and scripts for testing - As currently there is no proper way for the program to be tested for validity
- iOS export have different messages for when media is inserted, or a message is deleted - so changes need to be made in operations.py and flags.py
- Improve build.py
  - Remove inline comments (as the program is already removing other type of comments, so these should also get removed for uniformity)
  - Remove type hints (as some of its features only work in later versions, so some older versions can't execute the final script)

