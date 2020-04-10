"""Typing test implementation"""

from utils import *
from ucb import main, interact, trace
from datetime import datetime


###########
# Phase 1 #
###########


def choose(paragraphs, select, k):
    """Return the Kth paragraph from PARAGRAPHS for which SELECT called on the
    paragraph returns true. If there are fewer than K such paragraphs, return
    the empty string.
    """
    # BEGIN PROBLEM 1
    selected_list = [x for x in paragraphs if select(x)]
    if len(selected_list) < k + 1:
        return ''
    else:
        return selected_list[k]
    # END PROBLEM 1


def about(topic):
    """Return a select function that returns whether a paragraph contains one
    of the words in TOPIC.

    >>> about_dogs = about(['dog', 'dogs', 'pup', 'puppy'])
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup!'], about_dogs, 0)
    'Cute Dog!'
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup.'], about_dogs, 1)
    'Nice pup.'
    """
    assert all([lower(x) == x for x in topic]), 'topics should be lowercase.'
    # BEGIN PROBLEM 2
    def select_fun(paragraphs):
        strings = remove_punctuation(paragraphs)
        lower_strings = lower(strings)
        listed_strings = split(lower_strings)
        k = 0
        while k < len(listed_strings):
            for i in topic:
                if i == listed_strings[k]:
                    return True 
            k += 1 
        return False 







    return select_fun
    # END PROBLEM 2


def accuracy(typed, reference):
    """Return the accuracy (percentage of words typed correctly) of TYPED
    when compared to the prefix of REFERENCE that was typed.

    >>> accuracy('Cute Dog!', 'Cute Dog.')
    50.0
    >>> accuracy('A Cute Dog!', 'Cute Dog.')
    0.0
    >>> accuracy('cute Dog.', 'Cute Dog.')
    50.0
    >>> accuracy('Cute Dog. I say!', 'Cute Dog.')
    50.0
    >>> accuracy('Cute', 'Cute Dog.')
    100.0
    >>> accuracy('', 'Cute Dog.')
    0.0
    """
    typed_words = split(typed)
    reference_words = split(reference)
    # BEGIN PROBLEM 3
    if len(typed_words) == 0:
        return 0.0
    success = 0 
    if len(typed_words) <= len(reference_words):
        for i in range(len(typed_words)):
            if typed_words[i] == reference_words[i]:
                success += 1 
    else:
        for i in range(len(reference_words)):
            if typed_words[i] == reference_words[i]:
                success += 1 
    return success / len(typed_words) * 100
    # END PROBLEM 3


def wpm(typed, elapsed):
    """Return the words-per-minute (WPM) of the TYPED string."""
    assert elapsed > 0, 'Elapsed time must be positive'
    # BEGIN PROBLEM 4
    typed_len = len(typed)
    num_character = typed_len / 5 
    return num_character * (60.0 / elapsed)
    # END PROBLEM 4


def autocorrect(user_word, valid_words, diff_function, limit):
    """Returns the element of VALID_WORDS that has the smallest difference
    from USER_WORD. Instead returns USER_WORD if that difference is greater
    than LIMIT.
    """
    # BEGIN PROBLEM 5
    closest = user_word 
    new_list = []
    for i in valid_words:
        if i == user_word:
            return user_word 
    new_list = [x for x in valid_words if diff_function(user_word, x, limit) <= limit]
    if new_list == []:
        return user_word
    else:
        closest = min(new_list, key =lambda x: diff_function(user_word, x, limit))
    return closest
    # END PROBLEM 5


def swap_diff(start, goal, limit):
    """A diff function for autocorrect that determines how many letters
    in START need to be substituted to create GOAL, then adds the difference in
    their lengths.
    """
    # BEGIN PROBLEM 6
    start_list = list(start)
    goal_list = list(goal)
    difference = 0 
    k = limit
    if len(start_list) < len(goal_list):
        difference += len(goal_list) - len(start_list)
        goal_list = goal_list[:len(start_list)]
    else:
        difference += len(start_list) - len(goal_list)
        start_list = start_list[:len(goal_list)]

    def string_diff(list_start, list_goal, k, difference):
        if k < 0: 
            return limit + 1   
        elif list_start == []:
            return 0 
        else: 
            if list_start[0] != list_goal[0]:
                return 1 + string_diff(list_start[1:], list_goal[1:], k - 1, difference)
            else:
                return string_diff(list_start[1:], list_goal[1:], k, difference)


    return string_diff(start_list, goal_list, k, difference) + difference 
    # END PROBLEM 6

def edit_diff(start, goal, limit):
    """A diff function that computes the edit distance from START to GOAL."""

    if limit < 0:
        return limit + 1 

    if start == goal:
        return 0 

    if len(start) == 0 or len(goal) == 0:
        return len(start) + len(goal)

    if abs(len(goal) - len(start)) > limit:
        return limit + 1 

    if start[0] == goal[0]:
        return edit_diff(start[1:], goal[1:], limit)

    else:
        add_diff = 1 + edit_diff(start, goal[1:], limit - 1)  # Fill in these lines
        remove_diff = 1 + edit_diff(start[1:], goal, limit - 1)
        substitute_diff = 1 + edit_diff(start[1:], goal[1:], limit - 1)
        
        return min(add_diff, remove_diff, substitute_diff)


def final_diff(start, goal, limit):
    """A diff function. If you implement this function, it will be used."""
    assert False, 'Remove this line to use your final_diff function'




###########
# Phase 3 #
###########


def report_progress(typed, prompt, id, send):
    """Send a report of your id and progress so far to the multiplayer server."""
    # BEGIN PROBLEM 8
    progress = len(typed) / len(prompt)
    for i in range(len(typed)):
        if typed[i] != prompt[i]:
            progress = len(prompt[:i]) / len(prompt) 
            dictionary = {'id': id, 'progress': progress}
            send(dictionary)
            return progress
    dictionary = {'id': id, 'progress': progress}
    send(dictionary)
    return progress
    # END PROBLEM 8


def fastest_words_report(word_times):
    """Return a text description of the fastest words typed by each player."""
    fastest = fastest_words(word_times)
    report = ''
    for i in range(len(fastest)):
        words = ','.join(fastest[i])
        report += 'Player {} typed these fastest: {}\n'.format(i + 1, words)
    return report


def fastest_words(word_times, margin=1e-5):
    """A list of which words each player typed fastest."""
    n_players = len(word_times)
    n_words = len(word_times[0]) - 1
    assert all(len(times) == n_words + 1 for times in word_times)
    assert margin > 0
    # BEGIN PROBLEM 9
    """ megan's code"""
    t = 0
    all_times= []
    while t < n_players:
        times_for_player_t = []
        for i in range(1, len(word_times[t])):
            times_for_player_t += [elapsed_time(word_times[t][i]) - elapsed_time(word_times[t][i-1])]
        all_times += [times_for_player_t] 
        t += 1

    fastest_time = []
    word_count = 0
    while word_count < n_words: 
        times_for_word_i = []
        for player in range(n_players):
            times_for_word_i += [all_times[player][word_count]]
        fastest_time += [min(times_for_word_i)]
        word_count +=1 

    player = 0
    final_list = []
    while player < n_players:
        player_words = []
        for i in range(n_words): 
            if all_times[player][i] <= (fastest_time[i] + margin):
                player_words += [word(word_times[player][i + 1])]
        final_list += [player_words]
        player += 1

    return final_list
    








    
    # END PROBLEM 9


def word_time(word, elapsed_time):
    """A data abstrction for the elapsed time that a player finished a word."""
    return [word, elapsed_time]


def word(word_time):
    """An accessor function for the word of a word_time."""
    return word_time[0]


def elapsed_time(word_time):
    """An accessor function for the elapsed time of a word_time."""
    return word_time[1]


enable_multiplayer = False  # Change to True when you


##########################
# Command Line Interface #
##########################


def run_typing_test(topics):
    """Measure typing speed and accuracy on the command line."""
    paragraphs = lines_from_file('data/sample_paragraphs.txt')
    select = lambda p: True
    if topics:
        select = about(topics)
    i = 0
    while True:
        reference = choose(paragraphs, select, i)
        if not reference:
            print('No more paragraphs about', topics, 'are available.')
            return
        print('Type the following paragraph and then press enter/return.')
        print('If you only type part of it, you will be scored only on that part.\n')
        print(reference)
        print()

        start = datetime.now()
        typed = input()
        if not typed:
            print('Goodbye.')
            return
        print()

        elapsed = (datetime.now() - start).total_seconds()
        print("Nice work!")
        print('Words per minute:', wpm(typed, elapsed))
        print('Accuracy:        ', accuracy(typed, reference))

        print('\nPress enter/return for the next paragraph or type q to quit.')
        if input().strip() == 'q':
            return
        i += 1


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions."""
    import argparse
    parser = argparse.ArgumentParser(description="Typing Test")
    parser.add_argument('topic', help="Topic word", nargs='*')
    parser.add_argument('-t', help="Run typing test", action='store_true')

    args = parser.parse_args()
    if args.t:
        run_typing_test(args.topic)