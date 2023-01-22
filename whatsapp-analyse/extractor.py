"""
Here functions take in exported data from whatsapp and then makes it into Python object

data is a dict with key:value as -> name_of_person:(list of tuple -> (date, time, message))

For android the messages are in format -> 11/08/22, 11:50 am - Ayash Rath: Hi!
While in iOS the messages are in format -> [11/08/22, 11:50:00 AM] Ayash Rath: Hi!
Note - The above are called by me "message records"

And the time can be in either 12 hr or 24 hr format
The date can be in US or UK format
All the above need to be taken into consideration

Right now only android, with 12 hr format and uk date format is taken into consideration
"""

import re
import sys


# Regular expressions to detect if the string is start of a message record or a part of a message record
RE_DETECT_MESSG_ANDROID_12HR_UK: str = r"([0-2][0-9]|3[0-1])\/(0[0-9]|1[0-2])\/([2-9][0-9]), ([0-9]|1[0-2]):([0-5][0-9]) ([ap]m) - "


def extract_data(path: str) -> list:
    """
    Opens file and formats the data in a way for processing to take place
    It takes path of file and returns a list of messgs with all info intact (date, time, messg, messager)
    Note: some messages can have multiple lines so the code was not a simple for loop through the file
    """

    try:
        with open(path, encoding="utf-8") as file_handle:
            message_lst: list = []
            for line in file_handle:
                check_if_new_message: bool = not re.search(RE_DETECT_MESSG_ANDROID_12HR_UK, line) is None
                if check_if_new_message:
                    message_lst.append(line)
                else:
                    len_lst: int = len(message_lst)
                    message_lst[len_lst-1] += line
        return message_lst
    except FileNotFoundError:    # if file not found
        print("File Not Found")
        sys.exit()                # as pyinstaller doesn't understand quit()


def get_name_from_name_plus_messg(line: str) -> tuple:
    """
    Divides a message into name_of_sender and message if the message is in the following form
    (i.e, date and time information has been removed, i.e, clean_extracted_data's return data's element):
        > \"Ayash: POLL:\nIs Pi ≈ \nOPTION: 3.14 (5 votes)\nOPTION: 4.15 (0 votes)\n\n\"
    """

    pos_of_colon: int = line.find(":")
    if pos_of_colon != -1:                          ## For non-user messgaes like discription changed there is no colon used so we get -1
        name: str = line[0:pos_of_colon]
        message: str = line[pos_of_colon+2:]        ## it is +2 instead of +1 as after : there is a space in the data

        return (name, message)

    name = "Notification"
    message = line

    return (name, message)


def catagorise_data(extracted_data: list) -> dict:
    """
    catagorise the data into dict with key:value as -> name: list of tuple -> (date, time, messg)
    No specific functions to retrieve date and time from a line of message as they are simpler to obtain than name
    """

    main_dict: dict = {}

    for messg in extracted_data: # Right now the below if for android, 12 hr
        messg_split: str = messg.split(", ")
        date: str = messg.split(", ")[0]
        time: str = messg_split[1].split("-")[0]
        messg_plus_person: str = messg[20:].lstrip() # not using '-' as name may have '-' and also so using the fact that max date + time length = 20
        name, messg = get_name_from_name_plus_messg(messg_plus_person)
        main_dict[name] = main_dict.get(name, []) + [(date, time, messg)]

    return main_dict
