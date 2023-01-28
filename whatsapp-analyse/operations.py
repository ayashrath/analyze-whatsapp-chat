"""
these are functions which do the operations needed by the functions in flags.py

categorised_data_key  - (date, time, message)
"""

import re

# Used in stuff handling of links
#
STRINGS_USED_TO_IDENTIFY_LINKS: list[str] = ["http", ".com", ".org"]  # http also matches https
TOP_SITES: dict[str, list[str]] = {
    "YouTube": ["youtube.", "youtu.be"],
    "Google": ["google.", "goog.le", "g.co"],
    "Wikipedia": ["wikipedia."],
    "Meta's Sites": ["facebook.com", "fb.com", "instagram.com", "instagr.am", "whatsapp.com"],
    "Reddit": ["reddit.com"],
    "Twitter": ["twitter.com"],
    "Amazon": ["amazon."],
    "Yandex": ["yandex.ru"],
    "TicTok": ["tiktok."],
    "Bilibili": ["bilibili.com"],
    "News": ["cnn.com", "bbc.", "msn.com"],
}  # ending with . for some sites as, sites like YouTube have multiple domain names

# Special Messages that indicate if media was there in the message, message was deleted
#
STRING_USED_IN_PLACE_OF_MEDIA: str = "<Media omitted>"
STRING_USED_IN_PLACE_OF_DELETED_MESSG: str = "This message was deleted"
STRING_USED_IN_PLACE_OF_YOUR_DELETED_MESSG: str = "You deleted this message"

# REs
#
RE_FOR_ALL_WORDS: str = r'\w+'

# Used in notification flag - to find type of non-user message and sub-str to split message and find required info
#

# messg example: K changed the group description
# messg example: K started a video call
# messg example: K changed this group's icon
SEARCH_TERM_GRP_DESC_CHANGE: str = "changed the group description"
SEARCH_TERM_GRP_VIDEO_CALL: str = "started a video call"
SEARCH_TERM_GRP_ICON_CHANGE: str = "changed this group's icon"

# messg example: K created group "EX"
SEARCH_TERM_GRP_CREATOR: str = "created group"
SPLIT_TERM_GRP_CREATOR_NAME: str = "created"
SPLIT_TERM_GRP_CREATOR_GRP_NAME: str = "group"

# messg example: K changed the subject from  "EX" to "ex"
SEARCH_TERM_GRP_NAME_CHANGE: str = "changed the subject from"
SPLIT_TERM_GRP_NAME_CHANGE_NEW_NAME: str = "to"

# messg example: K added A
# message example: K joined using this group's invite link
SEARCH_TERM_GRP_MEMBER_ADD: str = "added"
SEARCH_TERM_GRP_MEMBER_JOIN_BY_LINK: str = "joined using this group's invite link"

# messg example: K removed A
# message example: K left
SEARCH_TERM_GRP_MEMBER_REMOVED: str = "removed"
SEARCH_TERM_GRP_MEMBER_LEFT: str = "left"


def get_first_and_last_date_ordered_list(categorised_data_key: list[tuple[str, str, str]]) -> tuple[str, str]:
    """
    It returns the first and last entry from a list of tuple containing date, time and message
    And it is ordered by date and time from oldest to earliest
    """

    oldest_date: str = categorised_data_key[0][0]
    newest_date: str = categorised_data_key[-1][0]

    return oldest_date, newest_date


def get_link_list(categorised_data_key: list[tuple[str, str, str]]) -> list[str]:
    """
    Get list of links from categorised_data_key
    Assumes that people don't write - text<link> with no whitespace in between
    """

    lst_of_links: list[str] = []

    for date_time_messg in categorised_data_key:
        messg = date_time_messg[2]
        link_found: bool = False

        for identifier in STRINGS_USED_TO_IDENTIFY_LINKS:
            if link_found:
                break  # If a link has both http and com it will give count of 2 so to prevent it
            for word in messg.split():
                if identifier in word:
                    lst_of_links.append(word.strip())  # no break here as a single message may have > 1 link
                link_found = True

    return lst_of_links


def count_link_list(link_lst: list[str]) -> dict[str, list[str]]:
    """
    Give count analysis of the link when list of links is passed through
    Uses user_defined dict for categorisation
    Uses top sites that people are most probably going to share
    """

    output_dict: dict[str, list[str]]
    output_dict = {}

    for link in link_lst:
        site_added: bool = False
        for site in TOP_SITES:
            if site_added:
                break
            for identifier in TOP_SITES[site]:
                if identifier in link and not site_added:
                    output_dict[site] = output_dict.get(site, []) + [link]
                    site_added = True
                    break
        if not site_added and link not in output_dict.get("Uncategorised", []):
            output_dict["Uncategorised"] = output_dict.get("Uncategorised", []) + [link]

    return output_dict


def clean_sorted_link_dict(sorted_link_dict: dict[str, list[str]]) -> dict[str, list[str]]:
    """
    Clean links in sorted link dict -> output of get_link_list ()
    It helps remove the parts of url for specific sites which are not important to access content
    It would be easy to remove everything after '?' but then this may break some links
    example - YouTube needs watch?v= to access the video
    """

    output_dict: dict[str, list[str]]
    output_dict = {}

    for site in sorted_link_dict:
        link_lst = sorted_link_dict[site]
        new_lst = []
        for link in link_lst:
            if site == "YouTube":
                if "youtube.com/watch?v" in link:  # Add elif(s) for a new site that requires ? to function
                    new_lst.append(link)
                    break

            pos_question_mark = link.find("?")

            if pos_question_mark != -1:
                link_to_add: str = link[:link.find("?")]
            else:  # As if there is no ? then returns -1 which would remove the last char of link if above used
                link_to_add = link

            if link_to_add[-1] == "/":  # To remove '/' at end in links as '/' don't serve a purpose in a link
                link_to_add = link_to_add[:-1]

            new_lst.append(link_to_add)

        output_dict[site] = new_lst

    return output_dict


def get_media_deleted_link_count(categorised_data_key: list[tuple[str, str, str]]) -> tuple[int, int, int]:
    """
    Get count of media, message deleted, links
    """

    media_counter: int = 0  # Counter variables
    deleted_counter: int = 0
    link_counter: int = 0

    for date_time_messg in categorised_data_key:
        messg = date_time_messg[2]
        if STRING_USED_IN_PLACE_OF_MEDIA in messg:
            media_counter += 1
        elif STRING_USED_IN_PLACE_OF_DELETED_MESSG in messg:
            deleted_counter += 1
        elif STRING_USED_IN_PLACE_OF_YOUR_DELETED_MESSG in messg:
            deleted_counter += 1
        else:
            link_counter = len(get_link_list(categorised_data_key))

    return media_counter, deleted_counter, link_counter


def longest_message_calculate(categorised_data_key: list[tuple[str, str, str]]) -> list[tuple[str, str, str]]:
    """
    Gets the largest message by total chars
    If 2 or more strings have the same length and are the longest - this still works
    """

    current_longest: list[tuple[str, str, str]]
    current_longest = []  # In case of more than 1 largest string
    length_of_current_longest: int = 0

    for date_time_messg in categorised_data_key:
        date: str = date_time_messg[0]
        time: str = date_time_messg[1]
        messg: str = date_time_messg[2]
        if len(messg) > length_of_current_longest:
            current_longest = [(date, time, messg)]
            length_of_current_longest = len(messg)
        elif len(messg) == length_of_current_longest:
            current_longest.append((date, time, messg))

    return current_longest


def sum_of_words(categorised_data_key: list[tuple[str, str, str]]) -> int:
    """
    Sum of all words from a list of string
    """

    total_words: int = 0
    for date_time_messg in categorised_data_key:
        messg: str = date_time_messg[2]
        total_words += len(re.findall(RE_FOR_ALL_WORDS, messg))  # Finds all the words in the string
    return total_words


def sum_of_char(categorised_data_key: list[tuple[str, str, str]]) -> int:
    """
    Sum of all chars from a list of string
    """

    total_char: int = 0
    for date_time_messg in categorised_data_key:
        messg: str = date_time_messg[2]
        for word in re.findall(RE_FOR_ALL_WORDS, messg):  # Finds all the words in the string
            total_char += len(word.strip())
    return total_char


def list_of_words(categorised_data_key: list[tuple[str, str, str]]) -> list[str]:
    """
    Make list of words from list of string
    It removes links from message string before extracting words in the message
    It also skips special messages like <media omitted> as they should not be used in the word count
    Returns list of words
    """

    link_list: list[str] = get_link_list(categorised_data_key)
    word_list: list[str] = []
    for date_time_messg in categorised_data_key:
        messg: str = date_time_messg[2]

        if messg in [STRING_USED_IN_PLACE_OF_MEDIA, STRING_USED_IN_PLACE_OF_DELETED_MESSG,
                     STRING_USED_IN_PLACE_OF_YOUR_DELETED_MESSG]:
            continue

        links_in_messg: list[str] = []
        for phrase in messg.split():
            if phrase in link_list:
                links_in_messg += [phrase]

        for link in links_in_messg:
            messg = messg.split(link)[-1]

        words_found: list[str] = re.findall(RE_FOR_ALL_WORDS, messg)  # Finds all the words in the string
        word_list += words_found
    return word_list


def clean_word_list(word_lst: list[str]) -> list[str]:
    """
    Uses output of list_of_words()
    Remove all repeated occurrences in a word list
    Returns a dictionary with format - word : count

    Assumption, words made of alphabets from any script
    """

    unique_word_lst: list[str] = []

    for word in word_lst:
        if any(not chars_in_word.isalpha() for chars_in_word in word):  # Checks if any non-alphabet present
            continue
        if word.lower() not in unique_word_lst:
            unique_word_lst += [word.lower()]

    return unique_word_lst


def get_word_count(word_lst: list[str]) -> dict[str, int]:
    """
        Uses output of list_of_words()
        Remove all repeated occurrences in a word list
        Clears out links and special messages like - <media omitted>
        Returns a dictionary with format - word : count

        returns dict with key:value -> word:count
        """

    word_dict: dict[str, int] = {}

    for word in word_lst:
        if any(not chars_in_word.isalpha() for chars_in_word in word):  # Checks if any non-alphabet present
            continue
        word_dict[word.lower()] = word_dict.get(word.lower(), 0) + 1

    return word_dict


def person_lst_of_word_to_word_lst_of_people(person_lst_of_word: dict[str, list[str]]) -> dict[str, list[str]]:
    """
    The aim of it is to convert dictionary of format - person: list_of unique_words, to the following:
        unique_word:list_of_people_who_used_it
    """
    return_dict: dict[str, list[str]] = {}

    for person in person_lst_of_word:
        for word in person_lst_of_word[person]:
            return_dict[word] = return_dict.get(word, []) + [person]

    return return_dict


def notif_data(categorised_data_key: list[tuple[str, str, str]]) -> dict:  # no more detail as values of different types
    """
    It goes through non-user messages and makes the data clearer

    Note:
    For Group Name change the data on who changed and what it was changed to can be obtained.
    so for that portion, only the way the name of the group changed over time and by whom is shown
    But for the rest, the data of what the change was doesn't exist so more focus has been but who
    made the changes
    """

    # We have both an individual counter and total counter, as in this case we want both, and didn't want
    # the individual parts to be computed to produce the total later
    data: dict = {
        "Group Creator": "",
        "Group Description Change": [0, {}],
        "Group Video Call": [0, {}],
        "Group Icon Change": [0, {}],
        "Group Name": [],
        "Member Add": [],
        "Member Subtract": []
    }

    for date_time_messg in categorised_data_key:
        date = date_time_messg[0]  # time is determined to be not a useful metric here
        messg = date_time_messg[2]

        # below ordered by expected chance of encounter, like here creator is at last as it will appear only once
        if SEARCH_TERM_GRP_VIDEO_CALL in messg:
            person_name: str = messg.split(SEARCH_TERM_GRP_VIDEO_CALL)[0]

            temp_get_data: list = data["Group Video Call"][1].get(person_name, [0, []])
            temp_get_data[0] += 1
            temp_get_data[1] += [date]
            data["Group Video Call"][1][person_name] = temp_get_data
            data["Group Video Call"][0] += 1

        elif SEARCH_TERM_GRP_ICON_CHANGE in messg:
            person_name = messg.split(SEARCH_TERM_GRP_ICON_CHANGE)[0]

            temp_get_data = data["Group Icon Change"][1].get(person_name, [0, []])
            temp_get_data[0] += 1
            temp_get_data[1] += [date]
            data["Group Icon Change"][1][person_name] = temp_get_data
            data["Group Icon Change"][0] += 1

        elif SEARCH_TERM_GRP_DESC_CHANGE in messg:
            person_name = messg.split(SEARCH_TERM_GRP_DESC_CHANGE)[0]

            temp_get_data = data["Group Description Change"][1].get(person_name, [0, []])
            temp_get_data[0] += 1
            temp_get_data[1] += [date]
            data["Group Description Change"][1][person_name] = temp_get_data
            data["Group Description Change"][0] += 1

        elif SEARCH_TERM_GRP_NAME_CHANGE in messg:
            name_changer: str = messg.split(SEARCH_TERM_GRP_NAME_CHANGE)[0].strip()
            data["Group Name"].append(
                (date, name_changer, messg.split(SPLIT_TERM_GRP_NAME_CHANGE_NEW_NAME)[-1].strip())
            )

        elif SEARCH_TERM_GRP_MEMBER_ADD in messg:
            split_message: list = messg.split(SEARCH_TERM_GRP_MEMBER_ADD)
            who_added_member: str = split_message[0].strip()
            new_member_name: str = split_message[1].strip().capitalize()  # To capitalize Y in "you" if it is = "you"
            data["Member Add"] += [(new_member_name, who_added_member, date)]

        elif SEARCH_TERM_GRP_MEMBER_JOIN_BY_LINK in messg:
            new_member_name = messg.split(SEARCH_TERM_GRP_MEMBER_JOIN_BY_LINK)[0].strip()
            who_added_member = "Joined by link"
            data["Member Add"] += [(new_member_name, who_added_member, date)]

        elif SEARCH_TERM_GRP_MEMBER_LEFT in messg:
            person_name_who_left: str = messg.split(SEARCH_TERM_GRP_MEMBER_LEFT)[0].strip()
            removed_by: str = "themselves"
            data["Member Subtract"] += [(person_name_who_left, removed_by, date)]

        elif SEARCH_TERM_GRP_MEMBER_REMOVED in messg:
            removed_by = messg.split(SEARCH_TERM_GRP_MEMBER_REMOVED)[0].strip()
            person_name_who_left = messg.split(SEARCH_TERM_GRP_MEMBER_REMOVED)[1].strip()
            data["Member Subtract"] += [(person_name_who_left, removed_by, date)]

        elif SEARCH_TERM_GRP_CREATOR in messg:
            data["Group Creator"] = messg.split(SPLIT_TERM_GRP_CREATOR_NAME)[0].strip()
            data["Group Name"].append(
                (date, data["Group Creator"], messg.split(SPLIT_TERM_GRP_CREATOR_GRP_NAME)[-1].strip())
            )

    return data
