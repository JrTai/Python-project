"""
Student code for Word Wrangler game
"""

import math
import urllib2
import codeskulptor
import poc_wrangler_provided as provided

WORDFILE = "assets_scrabble_words3.txt"


# Functions to manipulate ordered word lists

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.

    This function can be iterative.
    """
    ans = []
    for item in list1:
        if item not in ans:
            ans.append(item)
    return ans

def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    """
    ans = []
    for item in list1:
        lower = 0
        upper = len(list2)
        while lower + 1 < upper:
            mid = (lower + upper) / 2        
            if item < list2[mid]:
                upper = mid
            elif item > list2[mid]:
                lower = mid
            elif item == list2[mid]:
                ans.append(item)
                lower = upper
    return ans

# Functions to perform merge sort

def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing all of the elements that
    are in either list1 and list2.

    This function can be iterative.
    """ 
    ans = []
    temp_list1 = list(list1)
    temp_list2 = list(list2)
    while len(temp_list1) != 0 and len(temp_list2) != 0:
        if temp_list1[0] <= temp_list2[0]:
            ans.append(temp_list1[0])
            temp_list1.pop(0)
        elif temp_list2[0] <= temp_list1[0]:
            ans.append(temp_list2[0])
            temp_list2.pop(0)
    if  len(temp_list1) == 0:
        ans.extend(temp_list2)
    else:
        ans.extend(temp_list1)
    return ans
                
def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """
    if len(list1) == 0:
        return list1
    elif len(list1) == 1:
        return list1
    elif len(list1) == 2:
        return merge([list1[0]], [list1[1]])
    else:
        mid = int(math.floor(len(list1) / 2.))
        first_part = merge_sort(list1[:mid])
        second_part = merge_sort(list1[mid:])
        ans = merge(first_part,second_part)
        return ans

# Function to generate all strings for the word wrangler game

def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """
    if len(word) == 0:
        return [""]
    elif len(word) == 1:
        return [word, ""]
    else:
        first = str(word[0])
        rest_strings = []
        rest_strings += gen_all_strings(word[1:])
        new_string = []
        for each in rest_strings:
            if len(each) < 1:
                new_string.append(first)
            elif len(each) == 1:
                new_string.append(first + each)
                new_string.append(each + first)
            else:
                for index in range(len(each) - 1):
                    new_string.append(each[0:index + 1] + first + each[index + 1:])
                new_string.append(first + each)
                new_string.append(each + first)
        return rest_strings + new_string
        
# Function to load words from a file

def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    url = codeskulptor.file2url(filename)
    netfile = urllib2.urlopen(url)
    data_string = netfile.read()
    word_list = data_string.split()
    
    return word_list

def run():
    """
    Run game.
    """
    words = load_words(WORDFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates, 
                                     intersect, merge_sort, 
                                     gen_all_strings)
    provided.run_game(wrangler)

# Uncomment when you are ready to try the game
run()
  
    
