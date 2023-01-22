"""
This are the output and processing for all the flags
It also has functions which dictate how the values are printed out
"""

import sys
import json
import operations


# Print options -> functions which can be used to alter how certain value get printed out
# To make output look better

def int_comma_sep(number: float) -> str:
    """
    Make int into str with commas as seperators
    It also rounds long float no
    """

    rounded_float: float = round(number, 2)
    return f"{rounded_float:,}"



# Flag handling -> Functions for all the cli flags

def default_flag(categorised_data:dict) -> None:
    """
    handles the default flag data
    """

    for person in categorised_data:
        if person == "Notification":  # As we don't want any non-user stuff here
            continue

        person_data: list = categorised_data[person]
        counts: tuple = operations.get_media_deleated_link_count(person_data)
        no_words: int = operations.sum_of_words(person_data)
        no_chars: int = operations.sum_of_char(person_data)

        print("-" * len(person) + "--")
        print(person, ":")
        print("-" * len(person) + "--")
        print("No of messages sent in total = ", int_comma_sep(len(person_data)))
        print("No of messages deleted = ", int_comma_sep(counts[1]))
        print("No of photos, videos, audio or GIFs sent = ", int_comma_sep(counts[0]))
        print("No of link shared = ", int_comma_sep(counts[2]))
        print("Number of words used = ", int_comma_sep(no_words))
        print("Number of charcaters used = ", int_comma_sep((no_chars)))
        try:
            print("Average length of words = ", int_comma_sep(no_chars/no_words), "characters")
        except ZeroDivisionError:
            print("Average length of words = infinite characters")
        print("Average length of messages = ", int_comma_sep(no_words/len(person_data)), "words")
        print()


def total_flag(categorised_data:dict) -> None:
    """
    Handles for total data
    """
    total_messages: int = 0                  # Counter Vairables
    total_deleated: int = 0
    total_no_media: int = 0
    total_link_shared: int = 0
    total_words: int = 0
    total_chars: int = 0

    for person in categorised_data:
        person_data: list = categorised_data[person]
        counts: tuple = operations.get_media_deleated_link_count(person_data)
        no_words: int = operations.sum_of_words(person_data)
        no_chars: int = operations.sum_of_char(person_data)

        total_messages += len(person_data)
        total_deleated += counts[1]
        total_no_media += counts[0]
        total_link_shared += counts[2]
        total_words += no_words
        total_chars += no_chars

    print("------")
    print("Total :")
    print("------")
    print("No of messages sent in total = ", int_comma_sep(total_messages))
    print("No of messages deleted = ", int_comma_sep(total_deleated))
    print("No of photos, videos, audio or GIFs sent = ", int_comma_sep(total_no_media))
    print("No of link shared = ", int_comma_sep(total_link_shared))
    print("Number of words used = ", int_comma_sep(total_words))
    print("Number of charcaters used = ", int_comma_sep(total_chars))
    print("Average length of words = ", int_comma_sep(total_chars/total_words), "characters")
    print("Average length of messages = ", int_comma_sep(total_words/total_messages), "words")
    print()


def word_list_flag(categorised_data:dict) -> None:
    """
    Word Flag Handling
    """

    word_list: list = []

    for person in categorised_data:
        person_data: list = categorised_data[person]
        word_list += operations.list_of_words(person_data)

    final_dict: dict = operations.clean_word_list(word_list)

    print("-------------------------")
    print("Word List (" + int_comma_sep(len(final_dict)) + " words) :")
    print("-------------------------")
    print(json.dumps(final_dict, sort_keys=True, indent=4, ensure_ascii=False)) # To beautify the output, utf-8 allowed
    print()


def link_list_flag(catagorised_data: dict) -> None:
    """
    Link List Flag
    """

    total_link_lst: list = []

    for person in catagorised_data:
        if person == "Notification":  # As we don't want any non-user stuff here
            continue

        person_data = catagorised_data[person]
        needed_lst: list = operations.get_link_list(person_data)
        if needed_lst:
            total_link_lst += needed_lst

        cleaned_dict: dict = operations.clean_sorted_link_dict(operations.count_link_list(needed_lst))

        if not needed_lst:
            print("-" * len(person) + "--")
            print(person + " :")
            print("-" * len(person) + "--")
            print("No links shared!")
        else:
            print("-" * len(person) + "-------------")
            print(person + " (" + str(len(needed_lst)) + " links) :")
            print("-" * len(person) + "-------------")
            for site in cleaned_dict:
                print(site + " (" + str(len(cleaned_dict[site])) + " links): ")
                counter = 1
                for link in cleaned_dict[site]:
                    print(counter, ". ", link)
                    counter += 1
                print()
        print()


    total_cleaned_dict: dict = operations.clean_sorted_link_dict(operations.count_link_list(total_link_lst))

    print("-------------------")
    print("Total (" + str(len(total_link_lst)) + " links) :")
    print("-------------------")
    for site in total_cleaned_dict:
        print(site + " (" + str(len(total_cleaned_dict[site])) + " links): ")
        counter = 1
        for link in total_cleaned_dict[site]:
            print(counter, ". ", link)
            counter += 1
        print()
    print()


def notif_flag(categorised_data: dict) -> None:
    """
    Notification Flag Handling
    """

    person_data:list = categorised_data.get("Notification", [])

    if not person_data:
        print("There are no notification data")
        sys.exit()
    else:
        data = operations.notif_data(person_data)

    # Below if-else is used to handle cases where there were, for example no group icon change
    print("-------------------------------------------------------")
    print("Notification (You - The person who exported the data) :")
    print("-------------------------------------------------------")
    if not data["Group Creator"]:
        print("Information on who created the group could not be found")
    else:
        print("The Group was created by = ", data["Group Creator"])
    print()

    if not data["Group Name"]:
        print("Either group name has never changed, else group name change data couldn't be found")
    else:
        print("Group Name Change (" + int_comma_sep(len(data["Group Name"])) + " times):")
        counter = 1
        for record in data["Group Name"]:
            print(counter, ". ", record[2].strip(), "(" + record[1] +") - on", record[0])
            counter += 1
    print()

    if not data["Group Icon Change"][0]:
        print("Either group icon has never changed, else group icon change data couldn't be found")
    else:
        print("Group DP Change Record (" + int_comma_sep(data["Group Icon Change"][0]) + " times) =")
        for person in data["Group Icon Change"][1]:
            print(person + "(" + str(data["Group Icon Change"][1][person][0]), "times): ", data["Group Icon Change"][1][person][1])
    print()

    if not data["Group Discription Change"][0]:
        print("Either group description has never changed, else group description change data couldn't be found")
    else:
        print("Group Description Change Record (" + int_comma_sep(data["Group Discription Change"][0]) + " times) =")
        for person in data["Group Discription Change"][1]:
            print(person + "(" + str(data["Group Discription Change"][1][person][0]), "times): ", data["Group Discription Change"][1][person][1])
    print()

    if not data["Group Video Call"][0]:
        print("Either there have been no video calls, else video call data couldn't be found")
    else:
        print("Group Video Call Record (" + int_comma_sep(data["Group Video Call"][0]) + " times) =")
        for person in data["Group Video Call"][1]:
            print(person + "(" + str(data["Group Video Call"][1][person][0]), "times): ", data["Group Video Call"][1][person][1])
    print()


def length_flag(categorised_data: dict) -> None:
    """
    Length finding flag
    """

    individual_longest_messg: list = []
    person_longest_identifier: dict = {}

    for person in categorised_data:
        if person == "Notification":  # As we don't want any non-user stuff here
            continue

        person_data: list = categorised_data[person]
        longest_messg_data_lst: list = operations.longest_message_calculate(person_data)

        person_longest_identifier[person] = longest_messg_data_lst

        individual_longest_messg += longest_messg_data_lst

        print("-" * len(person) + "--")
        print(person + " :")
        print("-" * len(person) + "--")
        if len(longest_messg_data_lst) == 1:
            print("The longest message by the person (" + int_comma_sep(len(longest_messg_data_lst[0][2]))  + " chars long) = ")
            print("1. Date: " + longest_messg_data_lst[0][0])
            print("2. Time: " + longest_messg_data_lst[0][1])
            print("3. Message: \n\"" + longest_messg_data_lst[0][2].rstrip(), end="")
            print("\"", end="")
        else:
            counter = 1
            print("The longest message by the person (" + int_comma_sep(len(longest_messg_data_lst[0][2]))  + " chars long) = ")
            for messg in longest_messg_data_lst:
                print(counter)
                print("a. Date: " + messg[0])
                print("b. Time: " + messg[1])
                print("c. Message: \n \"" + messg[2].rstrip(), end = "")
                print("\"", end="")

        print("\n")

    longest_total_messg = operations.longest_message_calculate(individual_longest_messg)
    result_longest = []
    for person in person_longest_identifier:
        messg_lst = person_longest_identifier[person]
        for messg in messg_lst:
            if messg in longest_total_messg:
                result_longest.append((person, messg))

    print("------")
    print("Total :")
    print("------")
    if len(longest_total_messg) == 1:
        print("The total longest message (" + int_comma_sep(len(result_longest[0][1][2]))  + " characters long) = ")
        print("1. Date: " + result_longest[0][1][0])
        print("2. Time: " + result_longest[0][1][1])
        print("3. Message: \n\"" + result_longest[0][1][2].rstrip(), end="")
        print("\"", end="")
    else:
        counter = 1
        print("The total longest message (" + int_comma_sep(len(result_longest[0][1][2]))  + ") = ")

        for messg in result_longest:
            print(counter)
            print("\"", end="")
            print("1. Date: " + messg[1][0])
            print("2. Time: " + messg[1][1])
            print("3. Message: \n\"" + messg[1][2].rstrip(), end="")
            print("\"", end="")

    print() # Extra print as above doesn't end with \n
    print()
