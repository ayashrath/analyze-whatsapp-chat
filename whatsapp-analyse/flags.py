"""
These are the output and processing for all the flags
It also has functions which dictate how the values are printed out
"""

import sys
import json
import operations


# Print options -> functions which can be used to alter how certain value get printed out
# To make output look better


def int_comma_sep(number: float) -> str:
    """
    Make int into str with commas as separators
    It also rounds long float no
    """

    rounded_float: float = round(number, 2)
    return f"{rounded_float:,}"


def str_lst_to_str(lst_to_be_printed: list[str]) -> str:
    """
    Takes a short list of string like - ['11/08/22', '30/08/22']
    And returns -> '11/08/22, 30/08/22'
    """

    final_str: str = ""

    for element in lst_to_be_printed[:-1]:
        final_str += element + ", "
    final_str += lst_to_be_printed[-1]  # To avoid string to end with ','

    return final_str


# Flag handling -> Functions for all the cli flags
#
def default_flag(categorised_data: dict[str, list[tuple[str, str, str]]]) -> None:
    """
    handles the default flag data
    Note - It is not an option available in CLI but still I call it a flag as it is triggered in absence of other flags
    """

    no_of_people_in_chat_currently: int = len(categorised_data.keys())

    # If there are 2 people then it is a chat between 2 or group with 2, and if 1 then a group of 1
    if no_of_people_in_chat_currently > 2:  # In above cases this info is trivial so not printed out
        print("Number of people in group currently = " + int_comma_sep(no_of_people_in_chat_currently))
        print()

    print("_______________________________________________________")
    print("| # Overall analysis of member of chat individually - |")
    print("‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾")

    for person in categorised_data:
        if person == "Notification":  # As we don't want any non-user stuff here
            continue

        person_data: list[tuple[str, str, str]] = categorised_data[person]
        counts = operations.get_media_deleted_link_count(person_data)
        no_words = operations.sum_of_words(person_data)
        no_chars = operations.sum_of_char(person_data)
        oldest_messg_plus_newest_tuple = operations.get_first_and_last_date_ordered_list(person_data)

        print("-" * len(person) + "-----")
        print("##", person, ":")
        print("-" * len(person) + "-----")
        print("No of messages sent in total =", int_comma_sep(len(person_data)))
        print("No of messages deleted =", int_comma_sep(counts[1]))
        print("No of photos, videos, audio or GIFs sent =", int_comma_sep(counts[0]))
        print("No of link shared =", int_comma_sep(counts[2]))
        print("Number of words used =", int_comma_sep(no_words))
        print("Number of characters used =", int_comma_sep(no_chars))
        print("First message sent on =", oldest_messg_plus_newest_tuple[0])
        print("Last message sent on =", oldest_messg_plus_newest_tuple[1])
        try:
            print("Average length of words =", int_comma_sep(no_chars/no_words), "characters")
        except ZeroDivisionError:
            print("Average length of words = infinite characters")
        print("Average length of messages =", int_comma_sep(no_words/len(person_data)), "words")
        print()


def total_flag(categorised_data: dict[str, list[tuple[str, str, str]]]) -> None:
    """
    Handles for total data
    """
    total_messages: int = 0  # Counter Variable
    total_deleted: int = 0
    total_no_media: int = 0
    total_link_shared: int = 0
    total_words: int = 0
    total_chars: int = 0

    for person in categorised_data:
        person_data: list = categorised_data[person]
        counts: tuple = operations.get_media_deleted_link_count(person_data)
        no_words: int = operations.sum_of_words(person_data)
        no_chars: int = operations.sum_of_char(person_data)

        total_messages += len(person_data)
        total_deleted += counts[1]
        total_no_media += counts[0]
        total_link_shared += counts[2]
        total_words += no_words
        total_chars += no_chars

    print("_______________________________________________")
    print("| # Overall analysis of whole chat in total - |")
    print("‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾")

    print("----------")
    print("## Total :")
    print("----------")
    print("No of messages sent in total =", int_comma_sep(total_messages))
    print("No of messages deleted =", int_comma_sep(total_deleted))
    print("No of photos, videos, audio or GIFs sent =", int_comma_sep(total_no_media))
    print("No of link shared =", int_comma_sep(total_link_shared))
    print("Number of words used =", int_comma_sep(total_words))
    print("Number of characters used =", int_comma_sep(total_chars))
    print("Average length of words =", int_comma_sep(total_chars/total_words), "characters")
    print("Average length of messages =", int_comma_sep(total_words/total_messages), "words")
    print()


def word_list_flag(categorised_data: dict[str, list[tuple[str, str, str]]]) -> None:
    """
    Word Flag Handling
    """

    word_list: list = []

    for person in categorised_data:
        person_data: list = categorised_data[person]
        word_list += operations.list_of_words(person_data)

    final_dict: dict = operations.clean_word_list(word_list)

    print("______________________________________________")
    print("| # Word list for all messages in the chat - |")
    print("‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾")

    print("----------------------------")
    print("## Word List (" + int_comma_sep(len(final_dict)) + " words) :")
    print("----------------------------")
    print(json.dumps(final_dict, sort_keys=True, indent=4, ensure_ascii=False))  # To beautify the output, utf-8 allowed
    print()


def link_list_flag(categorised_data: dict[str, list[tuple[str, str, str]]]) -> None:
    """
    Link List Flag
    """

    total_link_lst: list = []

    print("______________________________________________")
    print("| # Link list for all messages in the chat - |")
    print("‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾")

    for person in categorised_data:
        if person == "Notification":  # As we don't want any non-user stuff here
            continue

        person_data = categorised_data[person]
        needed_lst: list = operations.get_link_list(person_data)
        if needed_lst:
            total_link_lst += needed_lst

        cleaned_dict: dict = operations.clean_sorted_link_dict(operations.count_link_list(needed_lst))

        if not needed_lst:
            print("-" * len(person) + "-----")
            print("##", person + " :")
            print("-" * len(person) + "-----")
            print("No links shared!")
        else:
            print("-" * len(person) + "----------------")
            print("##", person + " (" + str(len(needed_lst)) + " links) :")
            print("-" * len(person) + "----------------")
            for site in cleaned_dict:
                print(site + " (" + str(len(cleaned_dict[site])) + " links): ")
                counter = 1
                for link in cleaned_dict[site]:
                    print(int_comma_sep(counter) + ".", link)
                    counter += 1
                print()
        print()

    total_cleaned_dict: dict = operations.clean_sorted_link_dict(operations.count_link_list(total_link_lst))

    print("---------------------")
    print("## Total (" + str(len(total_link_lst)) + " links) :")
    print("---------------------")
    for site in total_cleaned_dict:
        print(site + " (" + str(len(total_cleaned_dict[site])) + " links): ")
        counter = 1
        for link in total_cleaned_dict[site]:
            print(int_comma_sep(counter) + ".", link)
            counter += 1
        print()
    print()


def notif_flag(categorised_data: dict[str, list[tuple[str, str, str]]]) -> None:
    """
    Notification Flag Handling
    """

    person_data: list = categorised_data.get("Notification", [])

    if not person_data:
        print("There are no notification data")
        sys.exit()
    else:
        data = operations.notif_data(person_data)

    print("_____________________________________")
    print("| # Analysis of non-user messages - |")
    print("‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾")

    # Below if-else is used to handle cases where there were, for example no group icon change
    # Order of print, ordered by how important it is
    print("----------------------------------------------------------")
    print("## Notification (\"You\" - Data exporter; ordered by date) :")  # Has 2 escape chars
    print("----------------------------------------------------------")
    if not data["Group Creator"]:
        print("Information on who created the group could not be found")
    else:
        print("The Group was created by =", data["Group Creator"])
    print()

    if not data["Member Add"]:
        print("Data on member who joined with group link, or were added couldn't be found")
    else:
        print("Member joining sequence (" + int_comma_sep(len(data["Member Add"])) + " additions):")
        counter = 1
        for member_add_tuple in data["Member Add"]:
            person_joined: str = member_add_tuple[0]
            added_by: str = member_add_tuple[1]
            date_of_join: str = member_add_tuple[2]

            if added_by == "Joined by link":
                print(int_comma_sep(counter) + ".", person_joined, "joined by link", "on", date_of_join)
            else:
                print(int_comma_sep(counter) + ".", person_joined, "was added by", added_by, "on", date_of_join)
            counter += 1
    print()

    if not data["Member Subtract"]:
        print("Data on member who joined with group link, or were added couldn't be found")
    else:
        print("Member leaving/getting removed sequence (" + int_comma_sep(len(data["Member Subtract"])) + " leaves):")
        counter = 1
        for member_subtract_tuple in data["Member Subtract"]:
            person_removed: str = member_subtract_tuple[0]
            removed_by: str = member_subtract_tuple[1]
            date_of_remove: str = member_subtract_tuple[2]

            if removed_by == "themselves":
                print(int_comma_sep(counter) + ".", person_removed, "left", "on", date_of_remove)
            else:
                print(int_comma_sep(counter) + ".", person_removed, "was removed by", removed_by, "on", date_of_remove)
            counter += 1
    print()

    if not data["Group Name"]:
        print("Either group name has never changed, else group name change data couldn't be found")
    else:
        print("Group Name Change (" + int_comma_sep(len(data["Group Name"])) + " times):")
        counter = 1
        for record in data["Group Name"]:
            new_grp_name_str: str = record[2].strip()
            who_gave_new_name: str = record[1]
            date_of_change: str = record[0]
            print(int_comma_sep(counter) + ".", new_grp_name_str, "(" + who_gave_new_name + ") - on", date_of_change)
            counter += 1
    print()

    if not data["Group Icon Change"][0]:
        print("Either group icon has never changed, else group icon change data couldn't be found")
    else:
        print("Group DP Change Record (" + int_comma_sep(data["Group Icon Change"][0]) + " times) =")
        for person in data["Group Icon Change"][1]:
            no_times_str: str = int_comma_sep(data["Group Icon Change"][1][person][0])
            date_str: str = str_lst_to_str(data["Group Icon Change"][1][person][1])
            print(person + "(" + no_times_str, "times):", date_str)
    print()

    if not data["Group Description Change"][0]:
        print("Either group description has never changed, else group description change data couldn't be found")
    else:
        print("Group Description Change Record (" + int_comma_sep(data["Group Description Change"][0]) + " times) =")
        for person in data["Group Description Change"][1]:
            no_times_str = int_comma_sep(data["Group Description Change"][1][person][0])
            date_str = str_lst_to_str(data["Group Description Change"][1][person][1])
            print(person + "(" + no_times_str, "times):", date_str)
    print()

    if not data["Group Video Call"][0]:
        print("Either there have been no video calls, else video call data couldn't be found")
    else:
        print("Group Video Call Record (" + int_comma_sep(data["Group Video Call"][0]) + " times) =")
        for person in data["Group Video Call"][1]:
            no_times_str = int_comma_sep(data["Group Video Call"][1][person][0])
            date_str = str_lst_to_str(data["Group Video Call"][1][person][1])
            print(person + "(" + no_times_str, "times):", date_str)
    print()


def length_flag(categorised_data: dict[str, list[tuple[str, str, str]]]) -> None:
    """
    Length finding flag
    """

    individual_longest_messg: list = []
    person_longest_identifier: dict = {}

    print("______________________________________")
    print("| # Analysis by length of messages - |")
    print("‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾")

    for person in categorised_data:
        if person == "Notification":  # As we don't want any non-user stuff here
            continue

        person_data: list = categorised_data[person]
        longest_messg_data_lst: list = operations.longest_message_calculate(person_data)

        person_longest_identifier[person] = longest_messg_data_lst

        individual_longest_messg += longest_messg_data_lst

        print("-" * len(person) + "-----")
        print("##", person + " :")
        print("-" * len(person) + "-----")
        if len(longest_messg_data_lst) == 1:
            print("The longest message by the person (" + int_comma_sep(len(longest_messg_data_lst[0][2])), "chars) =")
            print("1. Date: " + longest_messg_data_lst[0][0])
            print("2. Time: " + longest_messg_data_lst[0][1])
            print("3. Message: \n\"" + longest_messg_data_lst[0][2].rstrip(), end="")
            print("\"", end="")
        else:
            counter = 1
            print("The longest message by the person (" + int_comma_sep(len(longest_messg_data_lst[0][2])), "chars) =")
            for messg in longest_messg_data_lst:
                print(counter)
                print("a. Date: " + messg[0])
                print("b. Time: " + messg[1])
                print("c. Message: \n \"" + messg[2].rstrip(), end="")
                print("\"", end="")

        print("\n")

    longest_total_messg = operations.longest_message_calculate(individual_longest_messg)
    result_longest = []
    for person in person_longest_identifier:
        messg_lst = person_longest_identifier[person]
        for messg in messg_lst:
            if messg in longest_total_messg:
                result_longest.append((person, messg))

    print("----------")
    print("## Total :")
    print("----------")
    if len(longest_total_messg) == 1:
        print("The total longest message (" + int_comma_sep(len(result_longest[0][1][2])) + " characters long) = ")
        print("1. Date: " + result_longest[0][1][0])
        print("2. Time: " + result_longest[0][1][1])
        print("3. Message: \n\"" + result_longest[0][1][2].rstrip(), end="")
        print("\"", end="")
    else:
        counter = 1
        print("The total longest message (" + int_comma_sep(len(result_longest[0][1][2])) + ") = ")

        for messg in result_longest:
            print(counter)
            print("\"", end="")
            print("1. Date: " + messg[1][0])
            print("2. Time: " + messg[1][1])
            print("3. Message: \n\"" + messg[1][2].rstrip(), end="")
            print("\"", end="")

    print()  # Extra print as above doesn't end with \n
    print()
