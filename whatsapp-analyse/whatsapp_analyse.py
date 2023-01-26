"""
This is where the argparse part of code is
And here data extracted using functions of extractor.py is got and feeds into flags.py depending on user request
"""

import argparse
import extractor
import flags


def cli_implementation() -> dict:  # It has 2 types of value - str and bool, so no clean way to make it work, so skipped
    """
    This is all the code which implements the cli interface for the program
    """

    # Create a ArgumentParser
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Tool to analyse a WhatsApp Chat. \n Please refer "
                    "https://github.com/ayashrath/analyse-whatsapp-chat#extract-data for information on "
                    "exporting chat on mobile devices"
    )

    # Potion where all the arguments and flags of the CLI is listed and implemented
    parser.add_argument(
        "path",
        metavar="path",
        type=str,
        nargs=1,
        help="Path of Exported Text File of Chat",
    )
    parser.add_argument(
        "-n",
        "--notification",
        action="store_true",
        help="Obtain data on non-user messages (mainly in group chats) that occur in group chat, "
             "like a group's icon was changed",
    )
    parser.add_argument(
        "-t",
        "--total",
        action="store_true",
        help="Obtain data on the chat as a whole, in addition to data computed by default",
    )
    parser.add_argument(
        "-ll",
        "--list-link",
        action="store_true",
        help="Obtain data of links present in the chat)",
    )
    parser.add_argument(
        "-l",
        "--length",
        action="store_true",
        help="Obtain detailed results concerning length of message",
    )
    parser.add_argument(
        "-w",
        "--word-list",
        action="store_true",
        help="Obtain data on all words used, including how many times it was used and who used it",
    )
    arg: argparse.Namespace = parser.parse_args()

    result_dict: dict = {
        "path": arg.path[0],
        "total_bool": arg.total,
        "length_bool": arg.length,
        "word_list_bool": arg.word_list,
        "notification_bool": arg.notification,
        "link_list_bool": arg.list_link,
    }  # Holds the parsed data obtained from cli

    return result_dict


# Here the input in cli is put into variables
#
input_from_user = cli_implementation()
path: str = input_from_user["path"]
total_summary_needed: bool = input_from_user["total_bool"]
better_length_needed: bool = input_from_user["length_bool"]
word_list_needed: bool = input_from_user["word_list_bool"]
notification_needed: bool = input_from_user["notification_bool"]
link_list_needed: bool = input_from_user["link_list_bool"]

format_bool_tuple = extractor.data_format_android(path)
extracted_data = extractor.extract_data(path, format_bool_tuple[0], format_bool_tuple[1])
categorised_data = extractor.categorise_data(extracted_data, format_bool_tuple[0])


# Here all the flag gets checked and accordingly functions are called
# (ordered in the following way to give a good order to output in case multiple flags are activated)
# Order - default or Notification, default+total, better length, word list
# (Note - if default is true then no other output, and if it is not true then to get default you need to use --total)
#
default_case_checker: bool = (
    not total_summary_needed
    and not better_length_needed
    and not word_list_needed
    and not notification_needed
    and not link_list_needed
)


if default_case_checker:  # The default case = lack of presence of other flags
    flags.default_flag(categorised_data)
else:
    if notification_needed:
        flags.notif_flag(categorised_data)
    if total_summary_needed:
        flags.default_flag(categorised_data)
        flags.total_flag(categorised_data)
    if link_list_needed:
        flags.link_list_flag(categorised_data)
    if better_length_needed:
        flags.length_flag(categorised_data)
    if word_list_needed:
        flags.word_list_flag(categorised_data)

print("🎉🎉🎉 Done!")
