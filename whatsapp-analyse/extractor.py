"""
Here functions take in exported data from whatsapp and then makes it into Python object

Data is a dict with key:value as -> name_of_person:list of tuple -> (date, time, message)

Below need to be taken into consideration:
For android the messages are in format -> 11/08/22, 11:50 am - Ayash Rath: Hi!
While in iOS the messages are in format -> [11/08/22, 11:50:00 AM] Ayash Rath: Hi!
Note - The above are called by me "message records"

And the time can be in either 12 hr or 24 hr format

The date can be in US or UK format -> Ignored, as here we don't aim to do anything on the dates, so format they are
in becomes irrelevant
"""

import re
import sys


# Regular expressions to detect if the string is start of a message record or a part of a message record
# Date section is right for both UK and US date formats
RE_DETECT_MESSG_ANDROID_12HR: str = (
    r"([0-2][0-9]|3[0-1])\/([0-2][0-9]|3[0-1])\/((20)?[1-9][0-9]), "
    r"([0-9]|1[0-2]):([0-5]["r"0-9]) ([ap]m) - "
)
RE_DETECT_MESSG_ANDROID_24HR: str = (
    r"([0-2][0-9]|3[0-1])\/([0-2][0-9]|3[0-1])\/((20)?[1-9][0-9]), "
    r"([0-9]|1[0-9]|2[0-3]):([0-5][0-9]) - "
)
RE_DETECT_MESSG_IOS_12HR: str = (
    r"\[([0-2][0-9]|3[0-1])\/([0-2][0-9]|3[0-1])\/((20)?[1-9][0-9]), "
    r"([0-9]|1[0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9]) ([AP]M)\]"
)
RE_DETECT_MESSG_IOS_24HR: str = (
    r"\[([0-2][0-9]|3[0-1])\/([0-2][0-9]|3[0-1])\/((20)?[1-9][0-9]), "
    r"([0-9]|1[0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9])\]"
)


def data_format_android(path: str) -> tuple[bool, bool]:
    """
    It goes through the file in path it is passed and returns data format which will be needed later for extraction
    It returns -> True if android else false, which means iOS as the 2 possible options is Android and iOS
    """

    android_data_format: bool = False  # There are 2 possible outcomes, iOS or Android
    time_format_12_hr: bool = False  # There are 2 possible outcomes, 12-hr or 24-hr

    try:
        with open(path, encoding="utf-8") as file_handle:
            line1 = file_handle.readline()  # 1st line is guaranteed to be start of a message
            if line1[0] != "[":
                android_data_format = True
            for hr_12_checkers in [" AM] ", " PM] ", " am - ", " pm - "]:  # Not just 'am', etc; name may have 'am'/etc
                if hr_12_checkers in line1[:25]:  # As max date+time < 25
                    time_format_12_hr = True
                    break
    except FileNotFoundError:
        print("File Not Found")
        sys.exit()  # as pyinstaller doesn't understand quit()

    return android_data_format, time_format_12_hr


def extract_data(path: str, is_android: bool, is_12_hr: bool) -> list[str]:
    """
    Opens file and formats the data in a way for processing to take place
    It takes path of file and returns a list of messgs with all info intact (date, time, messg, messg sender)
    Note: some messages can have multiple lines so the code was not a simple for loop through the file
    """

    try:
        with open(path, encoding="utf-8") as file_handle:
            message_lst: list = []
            if is_android and is_12_hr:
                re_to_use: str = RE_DETECT_MESSG_ANDROID_12HR
            elif is_android and not is_12_hr:
                re_to_use = RE_DETECT_MESSG_ANDROID_24HR
            elif not is_android and is_12_hr:
                re_to_use = RE_DETECT_MESSG_IOS_12HR
            else:
                re_to_use = RE_DETECT_MESSG_IOS_24HR

            for line in file_handle:
                check_if_new_message: bool = not re.search(re_to_use, line) is None
                if check_if_new_message:
                    message_lst.append(line)
                else:
                    len_lst: int = len(message_lst)
                    message_lst[len_lst - 1] += line
    except FileNotFoundError:
        print("File Not Found")
        sys.exit()  # as pyinstaller doesn't understand quit()

    return message_lst


def get_name_from_name_plus_messg(line: str) -> tuple[str, str]:
    """
    Divides a message into name_of_sender and message if the message is in the following form
    (i.e, date and time information has been removed, i.e, clean_extracted_data's return data's element):
        > \"Ayash: POLL:\nIs Pi ≈ \nOPTION: 3.14 (5 votes)\nOPTION: 4.15 (0 votes)\n\n\"
    """

    pos_of_colon: int = line.find(":")
    if pos_of_colon != -1:  # For non-user messages like description changed there is no colon used, so we get -1
        name = line[0:pos_of_colon]
        message = line[pos_of_colon + 2:]  # it is +2 instead of +1 as after : there is a space in the data

        return name, message

    name = "Notification"
    message = line

    return name, message


def categorise_data(extracted_data: list, is_android: bool) -> dict[str, list[tuple[str, str, str]]]:
    """
    categorise the data into dict with key:value as -> name: list of tuple -> (date, time, messg)
    No specific functions to retrieve date and time from a line of message as they are simpler to obtain than name
    """

    main_dict: dict[str, list[tuple[str, str, str]]] = {}

    for messg in extracted_data:  # Right now the below if for android, 12 hr (note, names may have '-')
        if is_android:
            messg_split: str = messg.split(", ")  # Divides date and time+sender+message
            date: str = messg.split(", ")[0]
            time: str = messg_split[1].split("-")[0].rstrip()  # Divides time+sender+message to time and stores it
            messg_plus_person: str = messg[20:].lstrip()  # Using left-strip and fact len(max date + time) = 19/20
            name, messg = get_name_from_name_plus_messg(messg_plus_person)
            main_dict[name] = main_dict.get(name, []) + [(date, time, messg)]
        else:
            messg_split = messg.split(", ")  # Divides date and time+sender+message
            date = messg.split(", ")[0][1:]  # Removes [
            time = messg_split[1].split("]")[0]  # Divides time + sender + message to time and others and stores it
            messg_plus_person = messg_split[1].split("]")[1].lstrip()  # Removes time and adds rest
            name, messg = get_name_from_name_plus_messg(messg_plus_person)
            main_dict[name] = main_dict.get(name, []) + [(date, time, messg)]

    return main_dict
