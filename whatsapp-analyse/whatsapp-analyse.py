#!/usr/bin/env python3

"""
This is where the argparse part of code is there and here the processing is done by calling on functions from the other files
"""

import argparse
import extractor
import flags


# This is all the code which implements the cli interface for the program
#
def cli_implementation() -> dict:
    # Create a ArgumentParser
    parser:argparse.ArgumentParser = argparse.ArgumentParser(description="Tool to analyse a WhatsApp Chat \n Please refer https://github.com/ayashrath/analyse-whatsapp-chat#extract-data for information on exporting chat on mobile devices")

    # Potion where all the arguments and flags of the CLI is listed and implemented
    parser.add_argument("path", metavar="path", type=str, nargs=1, help="Path of Exported Text File of Chat")
    parser.add_argument("-t", "--total", action="store_true", help="Obtain data on the chat as a whole, in addition to data computed by default")
    parser.add_argument("-l", "--length", action="store_true", help="Obtain detailed results concerning length of message")
    parser.add_argument("-w", "--word-list", action="store_true", help="Obtain data on all words used, including how many times it was used and who used it")
    parser.add_argument("-n", "--notification", action="store_true", help="Obtain data on non-user messages that occur in group chat (example - message indicating that the group's description was changed)")
    parser.add_argument("-ll", "--list-link", action="store_true", help="Obtain data of links present in the chat)")
    arg:argparse.Namespace = parser.parse_args()


    result_dict: dict = {}  # Holds the parsed data obtained from cli
    result_dict["path"] = arg.path[0]
    result_dict["total_bool"] = arg.total
    result_dict["length_bool"] = arg.length
    result_dict["word_list_bool"] = arg.word_list
    result_dict["notification_bool"] = arg.notification
    result_dict["link_list_bool"] = arg.list_link


    return result_dict


# Here the input in cli is put into variables
#
input_from_user: dict = cli_implementation()
path: str = input_from_user["path"]
total_summary_needed: bool = input_from_user["total_bool"]
better_length_needed: bool = input_from_user["length_bool"]
word_list_needed:bool = input_from_user["word_list_bool"]
notification_needed: bool = input_from_user["notification_bool"]
link_list_needed: bool = input_from_user["link_list_bool"]

extracted_data: list = extractor.extract_data(path)
catagorised_data: dict = extractor.catagorise_data(extracted_data)

# Here all the flag gets checked and accordingly functions are called (ordered in the following way to give a good order to output in case multiple flags are activated)
# Order - default or Notification, default+total, better length, word list          (Note - if default is true then no other output, and if it is not true then to get default you need to use --total)
#
if total_summary_needed == better_length_needed == word_list_needed == notification_needed  == link_list_needed == False: # The default case
    flags.default_flag(catagorised_data)
else:
    if notification_needed:
        flags.notif_flag(catagorised_data)   
    if total_summary_needed:
        flags.default_flag(catagorised_data)
        flags.total_flag(catagorised_data)
    if link_list_needed:
        flags.link_list_flag(catagorised_data)
    if better_length_needed:
        flags.length_flag(catagorised_data)
    if word_list_needed:
        flags.word_list_flag(catagorised_data)

print()
print("Done!")