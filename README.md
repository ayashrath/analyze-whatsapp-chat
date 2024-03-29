# whatsapp-analyse: Parse and Analyse WhatsApp Chats

## Table of Content

- [Description](#description)
- [Installation](#installation)
- [Extract Data](#extract-data)
- [Usage](#usage)
- [Limitations](#limitations)
- [Making the Executables](#making-the-executables)
- [Project To-Do List](#project-to-do-list)
## Description

whatsapp-analyse is a command-line program to analyse personal or group WhatsApp chats. It requires Python3 to work and will work in all major operating systems.  
It is written procedurally with Python, i.e., without any user-defined classes.

## INSTALLATION

### For Windows

1. Download the whatsapp-analyse.exe file from releases ([Latest](https://github.com/ayashrath/analyze-whatsapp-chat/releases/download/v1.1/whatsapp-analyser.exe))
2. Then paste the whatsapp-analyse.exe file into any folder in the Windows path (To find the list, type - `echo %PATH%` in the command prompt) **except System32 folder**

### For macOS and Linux/GNU OSs

    sudo curl -L https://github.com/ayashrath/analyze-whatsapp-chat/releases/download/v1.1/whatsapp-analyser -o /usr/local/bin/whatsapp-analyser
    sudo chmod a+rx /usr/local/bin/whatsapp-analyser

If you don't want to use curl, you can use wget:

    sudo wget https://github.com/ayashrath/analyze-whatsapp-chat/releases/download/v1.1/whatsapp-analyser -O usr/local/bin/whatsapp-analyser
    sudo chmod a+rx usr/local/bin/whatsapp-analyser

## Extract Data

### Android

Please refer to the [WhatsApp FAQ Page](https://faq.whatsapp.com/1180414079177245) for information on the procedure to extract data for the analysis.

### iOS

1. Open the chat you want to get analysed
2. Click on the name of the person (or group name) which appears at the top after step 1
3. Scroll to the bottom to find a button for export
4. Use it to export the chat (Note: We don't need any media in our analysis, so try to get only the text file unless you wish to export the media files)
5. The file you get will be a .zip file, extract it and get the .txt file out of it - This file  is what we will be working on

## Usage

    usage: whatsapp_analyse.py [-h] [-n] [-t] [-ll] [-l] [-w {1,2,3}] path

    Tool to analyse a WhatsApp Chat. Please refer to https://github.com/ayashrath/analyse-whatsapp-chat#extract-data for information on the procedure to export chat on a mobile device.

    positional arguments:
      path                  path of exported text file of chat
    
    options:
      -h, --help            show this help message and exit
      -n, --notification    obtain data on non-user messages (specifically for group chats) that occur in group chat, like a group's icon was changed
      -t, --total           obtain data on the chat individually and as a whole
      -ll, --list-link      obtain categorised data of links present in the chat
      -l, --length          obtain detailed results concerning the length of messages
      -w {1,2,3}, --word-list {1,2,3}
                            obtain the list of unique words used [1 for just the list, 2 for 1 + count, and 3 for 2 + sender name]

### The default output of the tool

![Showcase Default Output](./media/default-flag.gif)

## Limitations

- Needs the user to export the whatsapp chat that needs to be analysed manually from a mobile device.
- It works only on the data available by exporting the chat from the mobile app, which means it will not work on deleted messages.
- It can't analyse data that may appear on your phone but is not in the exported .txt file. For example - in the app, we can see all the members in the group, but here we can only get a list of all the members who have their chat in the exported .txt file

## Making the Executables

1. Open the build.py file located in the tests directory.
2. Change the values of variables FILE_LST, MODULES_LST and BUILD_ON_UNIX_SYSTEM, if required.
3. Run the script, and you should get the file - whatsapp-analyse-full.
4. If on macOS or Linux, make them executable and use the shebang - `chmod +x whatsapp-analyse-full`.
5. For windows
    1. Install [PyInstaller](https://github.com/pyinstaller/pyinstaller).
    2. Clone this repository.
    3. Type in the command prompt or Powershell - `pyinstaller --noconfirm --onefile --console --clean whatsapp-analyse-full`.
    4. Then, the .exe file should be in the dist folder in the directory where you ran the above command.

## Project To-Do List

- New features to be added
  - Poll data analysis (new flag): Shows details of polls that were present in the group
  - Graphical analysis (new flag): Gives graphical analysis of appropriate areas
  - Date and time analysis (new flag): Makes use of the date and time data available
  - Full analysis report (new flag): Generates a full report in a single file for sharing purposes
  - Emoji count (in default and total flag): Gives a count of emojis
- Testing
  - New data for testing if everything works properly and validating changes
  - Scripts to do the testing
- iOS exports
  - in iOS exports the type of media can be identified, so type of media data needs to be added in the case of iOS exports
- Improve showcase GIF's quality
