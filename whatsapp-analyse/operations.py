"""
these are functions which do the operations needed by the functions in flags.py

categorised_data_key -> list of tuple -> (date, time, message)
"""


import re


# Remove links from categorised_data_key
# Assumes that prople don't write - text<link> with no whitespace in between
#
def delete_links(categorised_data_key: list) -> list:
    lst_of_links: list = []
    STRINGS_USED_TO_IDENTIFY_LINKS: list = ["http", ".com", ".org"] # https not used as if https in string then http must also be in the string

    for date_time_messg in categorised_data_key:
        messg = date_time_messg[2]
        link_found: bool = False

        for identifier in STRINGS_USED_TO_IDENTIFY_LINKS:
            if link_found:
                break # If a link has both http and com it will give count of 2 so to prevent it
            else:
                for word in messg.split():
                    if identifier in word:
                        lst_of_links.append(word.strip()) # Should not break here as a single message may habe +1 links 
                    link_found = True  
    
    return lst_of_links


# Get list of links from categorised_data_key
# Assumes that prople don't write - text<link> with no whitespace in between
#
def get_link_list(categorised_data_key: list) -> list:
    lst_of_links: list = []
    STRINGS_USED_TO_IDENTIFY_LINKS: list = ["http", ".com", ".org"] # https not used as if https in string then http must also be in the string

    for date_time_messg in categorised_data_key:
        messg = date_time_messg[2]
        link_found: bool = False

        for identifier in STRINGS_USED_TO_IDENTIFY_LINKS:
            if link_found:
                break # If a link has both http and com it will give count of 2 so to prevent it
            else:
                for word in messg.split():
                    if identifier in word:
                        lst_of_links.append(word.strip()) # Should not break here as a single message may habe +1 links 
                    link_found = True  
    
    return lst_of_links


# Give count analysis of the link when list of links is passed through
# Uses user_defined dict for catagorization
# Uses top sites that people are most probably going to share
#
def count_link_list(link_lst: list) -> dict: # not adding .com as websites like YouTube have multiple possible domain name so ending with '.' should be enough
    TOP_SITES: dict = {
        "YouTube" : ["youtube.", "youtu.be"],
        "Google" : ["google.", "goog.le", "g.co"], 
        "Wikipedia" : ["wikipedia."],
        "Meta's Sites" : ["facebook.com", "fb.com", "instagram.com", "instagr.am", "whatsapp.com"],
        "Reddit" : ["reddit.com"],
        "Twitter" : ["twitter.com"],
        "Amazon" : ["amazon."],
        "Yandex" : ["yandex.ru"],
        "TicTok" : ["tiktok."],
        "Bilibili" : ["bilibili.com"],
        "News" : ["cnn.com", "bbc.", "msn.com"]
    }

    output_dict = {}
    
    for link in link_lst:
        site_added: bool = False
        for site in TOP_SITES:
            if site_added:
                break
            for identifier in TOP_SITES[site]:
                if identifier in link and not site_added:
                    output_dict[site] = output_dict.get(site, []) + [link]
                    site_added: bool = True
                    break
        if not site_added and link not in output_dict.get("Uncatagorised", []):
            output_dict["Uncatagorised"] = output_dict.get("Uncatagorised", []) + [link]

    return output_dict


# Clean links in sorted link dict -> output of get_link_list ()
# It helps remove the parts of url for specific sites which are not important to access content
# It would be easy to remove everything after '?' but then this may break some links, ex - youtube needs watch?v= to access the video
#
def clean_sorted_link_dict(sorted_link_dict: dict) -> dict:
    output_dict: dict = {}

    for site in sorted_link_dict:
        link_lst = sorted_link_dict[site]
        new_lst = []
        for link in link_lst:
            if site == "YouTube":
                if "youtube.com/watch?v" in link: # Add elif and conditions if you add a new site to TOP_SITES in count_link_list and it requires ? to function
                    new_lst.append(link)
                    break
            new_lst.append(link[:link.find("?")])

        output_dict[site] = new_lst

    return output_dict



# Get count of media, message deleated, links
#
def get_media_deleated_link_count(categorised_data_key: list) -> tuple:
    media_counter: int = 0    # Counter variables
    deleated_counter: int = 0
    link_counter: int = 0

    STRING_USED_IN_PLACE_OF_MEDIA: str = "<Media omitted>"                         # Constant Variables
    STRING_USED_IN_PLACE_OF_DELETED_MESSG: str = "This message was deleted"
    STRING_USED_IN_PLACE_OF_YOUR_DELETED_MESSG: str = "You deleted this message"


    for date_time_messg in categorised_data_key:
        messg = date_time_messg[2]
        if STRING_USED_IN_PLACE_OF_MEDIA in messg:  # As in the text file in places where some form of media was sent this string is usually present
            media_counter += 1
        elif STRING_USED_IN_PLACE_OF_DELETED_MESSG in messg:
            deleated_counter += 1
        elif STRING_USED_IN_PLACE_OF_YOUR_DELETED_MESSG in messg:
            deleated_counter += 1
        else:
            link_counter = len(get_link_list(categorised_data_key))

    return (media_counter, deleated_counter, link_counter)


# Gets the largest message by total chars
# If 2 or more strings have the same length and are the longest - this still works
#
def longest_message_calculate(categorised_data_key: list) -> list:
    current_longest: list = []  # In case of more than 1 largest string
    length_of_current_longest: int = 0
    
    for date_time_messg in categorised_data_key:
        date: str = date_time_messg[0]
        time: str = date_time_messg[1]
        messg: str = date_time_messg[2]
        if len(messg) > length_of_current_longest:
            current_longest= [(date, time, messg)]
            length_of_current_longest = len(messg)
        elif len(messg) == length_of_current_longest:
            current_longest.append((date, time, messg))

    return current_longest


# Sum of all words from a list of string
#
def sum_of_words(categorised_data_key: list) -> int:
    total_words: int = 0
    for date_time_messg in categorised_data_key:
        messg: str = date_time_messg[2]
        total_words += len(re.findall(r'\w+', messg))   # This regular expression finds all the words in the string
    return total_words


# Sum of all chars from a list of string
#
def sum_of_char(categorised_data_key: list) -> int:
    total_char : int = 0
    for date_time_messg in categorised_data_key:
        messg: str = date_time_messg[2]
        for word in re.findall(r'\w+', messg):  # This regular expression finds all the words in the string
            total_char += len(word.strip())
    return total_char



# Make list of words from list of string
# Returns list of words
#
def list_of_words(categorised_data_key: list) -> list:
    word_list: list = []
    for date_time_messg in categorised_data_key:
        messg:str = date_time_messg[2]
        word_list += re.findall(r'\w+', messg)     # This regular expression finds all the words in the string
    return word_list


# Uses output of list_of_words()
# Remove all repeated occurances in a word list 
# Returns a dictionary with format - word : count
#
def clean_word_list(word_lst: list) -> dict:
    word_dict: dict = {}

    for word in word_lst:
        if any(not chars_in_word.isalpha() for chars_in_word in word): # Assumption, no words have digits or chars like _ in them
            continue
        else:
            word_dict[word.lower()] = word_dict.get(word.lower(), 0) + 1

    return word_dict