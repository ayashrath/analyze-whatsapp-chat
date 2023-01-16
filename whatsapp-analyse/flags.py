"""
This are the output and processing for all the flags
It also has functions which dictate how the values are printed out
"""

import operations
import json


# Print options -> functions which can be used to alter how certain value get printed out

# Make int into str with commas as seperators
# It also rounds long float no
#
def int_comma_sep(no: float) -> str:
    rounded_float: float = round(no, 2)
    return f"{rounded_float:,}"



# Flag handling -> Functions for all the cli flags

# handles the default flag data
#
def default_flag(categorised_data:dict) -> None:
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
        except:
            print("Average length of words = infinite characters")
        print("Average length of messages = ", int_comma_sep(no_words/len(person_data)), "words")
        print()
        print()


# Handles for total data
#
def total_flag(categorised_data:dict) -> None:
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


# Word Flag Handling
#
def word_list_flag(categorised_data:dict) -> None:
    word_list: list = []

    for person in categorised_data:
        person_data: list = categorised_data[person]
        word_list += operations.list_of_words(person_data)

    final_dict: dict = operations.clean_word_list(word_list)

    print("-------------------------")
    print("Word List (" + int_comma_sep(len(final_dict)) + " words) :")
    print("-------------------------")
    print(json.dumps(final_dict, sort_keys=True, indent=4, ensure_ascii=False))         # To beautify the output



# Notification Flag Handling
#
def notif_flag(categorised_data: dict) -> None:
    grp_creator: str = ""
    no_discription_change: int = 0        # Both counter variable and record variables
    discription_change_record: dict = {}
    no_video_calls: int = 0
    video_call_record: dict = {}
    grp_name_change: list = []
    no_grp_icon_change: int = 0
    grp_icon_change_record: dict = {}

    for person in categorised_data:
        if person == "Notification":  # Prepared to parse correctly according to the standard that whatsapp uses for non-user messgaes as on 6th January 2023
            person_data: list = categorised_data[person]
            for messg_data in person_data:
                date = messg_data[0] # time is determined to be not a useful matric here                                   
                messg = messg_data[2]
                if "changed the group description" in messg: # Example of a message where discription is changed to follow along what the function does -> 27/12/22, 6:41 pm - K changed the group description
                    temp_get_data: list = discription_change_record.get(messg.split("changed")[0], [0, []])
                    temp_get_data[0] += 1
                    temp_get_data[1] += [date]
                    discription_change_record[messg.split("changed")[0]] = temp_get_data
                    no_discription_change += 1
                elif "started a video call" in messg: # Example of a message where video call is started to follow along what the function does -> 29/08/22, 10:15 am - K started a video call
                    temp_get_data: list = video_call_record.get(messg.split("started")[0], [0, []])
                    temp_get_data[0] += 1
                    temp_get_data[1] += [date]
                    video_call_record[messg.split("started")[0]] = temp_get_data
                    no_video_calls += 1
                elif "changed this group's icon" in messg: # Example of a message where group icon is changed to follow along what the function does -> 05/09/22, 6:37 am - K changed this group's icon
                    temp_get_data: list = grp_icon_change_record.get(messg.split("changed")[0], [0, []])
                    temp_get_data[0] += 1
                    temp_get_data[1] += [date]
                    grp_icon_change_record[messg.split("changed")[0]] = temp_get_data
                    no_grp_icon_change += 1
                elif "created group" in messg: # It does both extract group name and creator name; example text -> 11/08/22, 5:35 am - K created group "EXAMPLE"
                    print(messg)
                    grp_creator = messg.split(" created ")[0]
                    grp_name_change.append((date, grp_creator, messg.split("group ")[-1]))
                elif "changed the subject from" in messg: # Example - 30/08/22, 11:09 am - K changed the subject from  "EXAMPLE" to "example"
                    name_changer: str = messg.split(" changed ")[0]
                    grp_name_change.append((date, name_changer, messg.split(" to ")[-1]))
    
    # Below if-else is used to handle cases where there were, for example no group icon change
    print("-------------------------------------------------------")
    print("Notification (You - The person who exported the data) :")
    print("-------------------------------------------------------")
    if grp_creator == "Information on who created the group could not be found":
        pass
    else:
        print("The Group was created by = ", grp_creator)
    print()

    if len(grp_name_change) == 0:
        print("Either group name has never changed, else group name change data couldn't be found")
    else:
        print("Group Name Change (" + int_comma_sep(len(grp_name_change)) + " times):")

    if grp_name_change == []:
        pass
    else:
        counter = 1
        for record in grp_name_change: # Not using list comprehension as for the number I need to use .index() which messes up the output sometimes (not checked by though)
            print(counter, ". ", record[2].strip(), "(" + record[1] +") - on", record[0])
            counter += 1
    print()
    
    if no_grp_icon_change == 0:
        print("Either group icon has never changed, else group icon change data couldn't be found")
    else:
        print("Group DP Change Record (" + int_comma_sep(no_grp_icon_change) + " times) =")
        [print(person + "(" + str(grp_icon_change_record[person][0]), "times): ", grp_icon_change_record[person][1]) for person in grp_icon_change_record]
    print()
    
    if no_discription_change == 0:
        print("Either group description has never changed, else group description change data couldn't be found")
    else:
        print("Group Description Change Record (" + int_comma_sep(no_discription_change) + " times) =")
        [print(person + "(" + str(discription_change_record[person][0]), "times): ", discription_change_record[person][1]) for person in discription_change_record]
    print()
    
    if no_video_calls == 0:
        print("Either there have been no video calls, else video call data couldn't be found")
    else:
        print("Group Video Call Record (" + int_comma_sep(no_video_calls) + " times) =")
        [print(person + "(" + str(video_call_record[person][0]), "times): ", video_call_record[person][1]) for person in video_call_record]
    print()
    print()


# Length finding flag
#
def length_flag(categorised_data: dict) -> None:
    longest_total_messg: list = []
    person_longest_identifier = {}

    for person in categorised_data:
        if person == "Notification":  # As we don't want any non-user stuff here
            continue

        person_data: list = categorised_data[person]
        longest_messg_data_lst: list = operations.longest_message_calculate(person_data) 

        person_longest_identifier[person] = longest_messg_data_lst

        longest_total_messg += longest_messg_data_lst

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

    longest_total_messg: list = operations.longest_message_calculate(longest_total_messg)
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

    print()
    print()


# Link List Flag
#
def link_list_flag(catagorised_data: dict) -> None:
    total_link_lst: list = []

    for person in catagorised_data:
        if person == "Notification":  # As we don't want any non-user stuff here
            continue

        person_data = catagorised_data[person]
        needed_lst: list = operations.get_link_list(person_data)
        if needed_lst != []:
            total_link_lst += needed_lst

        cleaned_dict: dict = operations.clean_sorted_link_dict(operations.count_link_list(needed_lst))

        if needed_lst == []:
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