"""
Here functions are defined which take in exported data from whatsapp and then makes it into Python object

data is a dict with key:value as -> name_of_person:(list of tuple -> (date, time, message))
"""

import re
import sys



# Opens file and formats the data in a way for processing to take place
# It takes the file and returns a list of messgaes with all information intact (i.e, date, time, person who messaged, message)
# Note: some messages can have multiple lines so the code was not a simple for loop through the file
#
def extract_data(path: str) -> list:
    try:
        with open(path, encoding="utf-8") as fh:
            message_lst: list = []
            for line in fh:
                re_for_check:str = r"([0-2][0-9]|3[0-1])\/(0[0-9]|1[0-2])\/([2-9][0-9]), ([0-9]|1[0-2]):([0-5][0-9]) ([ap]m) - "  # This is regex for date and time as found in whatsapp export text
                check_if_new_message: bool = False if re.search(re_for_check, line) == None else True
                if check_if_new_message: 
                    message_lst.append(line)
                else:
                    len_lst: int = len(message_lst)
                    message_lst[len_lst-1] += line
        return message_lst
    except FileNotFoundError:    # if file not found
        print("File Not Found")
        sys.exit()                # as pyinstaller doesn't understand quit()


# Divides a message into name_of_sender and message if the message is in the following form (i.e, date and time information has been removed, i.e, clean_extracted_data's return data's element):
#    Ayash: POLL:\nIs Pi ≈ \nOPTION: 3.14 (5 votes)\nOPTION: 4.15 (0 votes)\n\n
#
def get_name_from_name_plus_messg(line: str) -> tuple:
    pos_of_colon: int = line.find(":")
    if pos_of_colon != -1:                          ## For non-user messgaes like discription changed there is no colon used so we get -1
        name: str = line[0:pos_of_colon]
        message: str = line[pos_of_colon+2:]        ## it is +2 instead of +1 as after : there is a space in the data

        return (name, message)

    else:
        name: str = "Notification"
        message: str = line

        return (name, message)


# catagorise the data into dict with key:value as -> name: list of tuple -> (date, time, messg)
# No specific functions to retrieve date and time from a line of message as they are simpler to obtain than name
#
def catagorise_data(extracted_data: list) -> dict:
    main_dict: dict = {}

    for messg in extracted_data:
        messg_split: str = messg.split(", ")
        date: str = messg.split(", ")[0]
        time: str = messg_split[1].split("-")[0]
        messg_plus_person: str = messg[20:].lstrip() # not using '-' as name may have '-' and also so using the fact that max date + time length = 20
        name, messg = get_name_from_name_plus_messg(messg_plus_person)
        main_dict[name] = main_dict.get(name, []) + [(date, time, messg)]

    return main_dict

