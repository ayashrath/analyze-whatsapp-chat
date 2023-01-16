# whatsapp-analyse: Parse and Analyse WhatsApp Chats

[comment]: <> (Add gif where it is being used)

## Table of Content

- [Description](#description)
- [Installation](#installation)
- [Extract Data](#extract-data)
- [Usage](#usage)
- [Building and Testing](#building-and-testing)

## Description

whatsapp-analyse is a command-line program to analyse personal or group WhatsApp chats. It requires python3 to work and will work in all major operating systems.

## INSTALLATION

### For Windows (generated with [PyInstaller](https://github.com/pyinstaller/pyinstaller))

1. Download the whatsapp-analyse.exe file from releases (recommended - use the latest).
2. Then paste the whatsapp-analyse.exe file into any folder in Windows path (To find the list type - `echo %PATH%` in command prompt) **except System32 folder**

### For Unix Based OS (MacOS and Linux/GNU OSs)

    sudo curl -L https://raw.githubusercontent.com/ayashrath/analyse-whatsapp-chat/master/whatsapp-analyser.py -o /usr/local/bin/whatsapp-analyser
    sudo chmod a+rx /usr/local/bin/whatsapp-analyser

If you gon't have curl, you can use wget:

    sudo wget https://raw.githubusercontent.com/ayashrath/analyse-whatsapp-chat/master/whatsapp-analyser.py -O usr/local/bin/whatsapp-analyser
    sudo chmod a+rx usr/local/bin/whatsapp-analyser

## Extract Data

### Android

Please refer to the [WhatsApp FAQ Page](https://faq.whatsapp.com/1180414079177245) for information on how to extract data which needs to be analysed

### iOS

1. Open the chat you want to get analysed
2. Click on the name of the person (or group name) which appears in the top after step 1
3. Scroll to the bottom to find a button for export
4. Use it to export the chat -> we don't need media to be included wih out export
5. The file you get will a .zip file, extract it and get the .txt file out of it - This file  is what we will be working on

## Usage

    $ whatsapp-analyse --help 

    usage: whatsapp-analyse-full [-h] [-t] [-l] [-w] [-n] [-ll] path

    Tool to analyse a WhatsApp Chat Please refer https://github.com/ayashrath/analyse-whatsapp-chat#extract-data for information on exporting chat on mobile devices

    positional arguments:
    path                Path of Exported Text File of Chat

    options:
      -h, --help          show this help message and exit
      -t, --total         Obtain data on the chat as a whole, in addition to data computed by default
      -l, --length        Obtain detailed results concerning length of message
      -w, --word-list     Obtain data on all words used, including how many times it was used and who used it
      -n, --notification  Obtain data on non-user messages that occur in group chat (example - message indicating that the group's description was changed)
      -ll, --list-link    Obtain data of links present in the chat)

For basic indiviual member's analysis (example.txt can be found in repo's root directory):

    $ whatsapp-analyse example.txt

    ---
    R :
    ---
    No of messages sent in total =  2
    No of messages deleted =  0
    No of photos, videos, audio or GIFs sent =  0
    No of link shared =  0
    Number of words used =  3
    Number of charcaters used =  11
    Average length of words =  3.67 characters
    Average length of messages =  1.5 words
    
    
    ---
    B :
    ---
    No of messages sent in total =  9
    No of messages deleted =  1
    No of photos, videos, audio or GIFs sent =  1
    No of link shared =  0
    Number of words used =  35
    Number of charcaters used =  135
    Average length of words =  3.86 characters
    Average length of messages =  3.89 words
    
    
    ---
    K :
    ---
    No of messages sent in total =  1
    No of messages deleted =  0
    No of photos, videos, audio or GIFs sent =  0
    No of link shared =  0
    Number of words used =  6
    Number of charcaters used =  13
    Average length of words =  2.17 characters
    Average length of messages =  6.0 words
    
    
    
    Done!

## Building and Testing

### To make a single executable from project files

1. Open the build-final.py file located in tests directory
2. Change the values of variables FILE_LST and MODULES_LST, if required
3. Run the script and you should get file - whatsapp-analyse-full
4. If on MacOS or Linux, to make them executable and use the shabang - `chmod +x whatsapp-analyse-full`
5. For windows
    1. Install pyinstaller by typing this out in command prompt or Powershell - `pip install pyinstaller`  
    2. Clone this repository  
    3. Then type this in command prompt or Powershell - `pyinstaller --noconfirm --onefile --console --clean path_of_whatsapp-analyse.py`  
    4. Then the .exe file can be found in the dist folder in the directory where you ran the above command

## Features to add / Bugs to solve

- New flags
  - emoji count
  - poll data analysis
  - graphical analysis
  - date and time analysis
    - most active date
    - time analysis
  - Full analysis report return
- impoved word list
- iOS .txt support
- windows build-final.py support
- UK and US date formats -> date info extract in extractor.py
- better data and scripts for testing