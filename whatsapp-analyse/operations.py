"""
these are functions which do the operations needed by the functions in flags.py

categorised_data_key -> list of tuple -> (date, time, message)
"""

import re


# Used in stuff handling of links
#
STRINGS_USED_TO_IDENTIFY_LINKS: list = ["http", ".com", ".org"]  # http also matches https
TOP_SITES: dict = {
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
        "News": ["cnn.com", "bbc.", "msn.com"]
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
SEARCH_TERM_GRP_DESC_CHANGE: str = "changed the group description"  # messg example: K changed the group description
SEARCH_TERM_GRP_VIDEO_CALL: str = "started a video call"  # messg example: K started a video call
SEARCH_TERM_GRP_ICON_CHANGE: str = "changed this group's icon"  # messg example: K changed this group's icon

SEARCH_TERM_GRP_CREATOR: str = "created group"  # messg example: K created group "EXAMPLE"
SPLIT_TERM_GRP_CREATOR_NAME: str = "created"
SPLIT_TERM_GRP_CREATOR_GRP_NAME: str = "group"

SEARCH_TERM_GRP_NAME_CHANGE: str = "changed the subject from"  # messg example: K changed the subject from  "EXAMPLE" to "example"
SPLIT_TERM_GRP_NAME_CHANGE_NEW_NAME: str = "to"


def get_link_list(categorised_data_key: list) -> list:
    """
    Get list of links from categorised_data_key
    Assumes that people don't write - text<link> with no whitespace in between
    """

    lst_of_links: list = []

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


def count_link_list(link_lst: list) -> dict:
    """
    Give count analysis of the link when list of links is passed through
    Uses user_defined dict for categorisation
    Uses top sites that people are most probably going to share
    """

    output_dict: dict = {}

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


def clean_sorted_link_dict(sorted_link_dict: dict) -> dict:
    """
    Clean links in sorted link dict -> output of get_link_list ()
    It helps remove the parts of url for specific sites which are not important to access content
    It would be easy to remove everything after '?' but then this may break some links
    example - YouTube needs watch?v= to access the video
    """
    output_dict: dict = {}

    for site in sorted_link_dict:
        link_lst = sorted_link_dict[site]
        new_lst = []
        for link in link_lst:
            if site == "YouTube":
                if "youtube.com/watch?v" in link:  # Add elif(s) for a new site that requires ? to function
                    new_lst.append(link)
                    break
            new_lst.append(link[:link.find("?")])

        output_dict[site] = new_lst

    return output_dict


def get_media_deleted_link_count(categorised_data_key: list) -> tuple:
    """
    Get count of media, message deleted, links
    """

    media_counter: int = 0    # Counter variables
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


def longest_message_calculate(categorised_data_key: list) -> list:
    """
    Gets the largest message by total chars
    If 2 or more strings have the same length and are the longest - this still works
    """

    current_longest: list = []  # In case of more than 1 largest string
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


def sum_of_words(categorised_data_key: list) -> int:
    """
    Sum of all words from a list of string
    """

    total_words: int = 0
    for date_time_messg in categorised_data_key:
        messg: str = date_time_messg[2]
        total_words += len(re.findall(RE_FOR_ALL_WORDS, messg))  # Finds all the words in the string
    return total_words


def sum_of_char(categorised_data_key: list) -> int:
    """
    Sum of all chars from a list of string
    """

    total_char: int = 0
    for date_time_messg in categorised_data_key:
        messg: str = date_time_messg[2]
        for word in re.findall(RE_FOR_ALL_WORDS, messg):  # Finds all the words in the string
            total_char += len(word.strip())
    return total_char


def list_of_words(categorised_data_key: list) -> list:
    """
    Make list of words from list of string
    Returns list of words
    """

    word_list: list = []
    for date_time_messg in categorised_data_key:
        messg: str = date_time_messg[2]
        word_list += re.findall(RE_FOR_ALL_WORDS, messg)  # Finds all the words in the string
    return word_list


def clean_word_list(word_lst: list) -> dict:
    """
    Uses output of list_of_words()
    Remove all repeated occurrences in a word list
    Returns a dictionary with format - word : count

    Assumption, words made of alphabets from any script
    """

    word_dict: dict = {}

    for word in word_lst:
        if any(not chars_in_word.isalpha() for chars_in_word in word):  # Checks if any non-alphabet present
            continue
        word_dict[word.lower()] = word_dict.get(word.lower(), 0) + 1

    return word_dict


def notif_data(categorised_data_key: list) -> dict:
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
        "Group Name": []
    }

    for date_time_messg in categorised_data_key:
        date = date_time_messg[0]  # time is determined to be not a useful metric here
        messg = date_time_messg[2]

        if SEARCH_TERM_GRP_DESC_CHANGE in messg:
            person_name: str = messg.split(SEARCH_TERM_GRP_DESC_CHANGE)[0]

            temp_get_data: list = data["Group Description Change"][1].get(person_name, [0, []])
            temp_get_data[0] += 1
            temp_get_data[1] += [date]
            data["Group Description Change"][1][person_name] = temp_get_data

            data["Group Description Change"][0] += 1
        elif SEARCH_TERM_GRP_VIDEO_CALL in messg:
            person_name = messg.split(SEARCH_TERM_GRP_VIDEO_CALL)[0]

            temp_get_data = data["Group Video Call"][1].get(person_name, [0, []])
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
        elif SEARCH_TERM_GRP_NAME_CHANGE in messg:
            name_changer: str = messg.split(SEARCH_TERM_GRP_NAME_CHANGE)[0].strip()
            data["Group Name"].append((date, name_changer, messg.split(SPLIT_TERM_GRP_NAME_CHANGE_NEW_NAME)[-1]))
        elif SEARCH_TERM_GRP_CREATOR in messg:
            data["Group Creator"] = messg.split(SPLIT_TERM_GRP_CREATOR_NAME)[0].strip()
            data["Group Name"].append((date, data["Group Creator"], messg.split(SPLIT_TERM_GRP_CREATOR_GRP_NAME)[-1]))

    return data
