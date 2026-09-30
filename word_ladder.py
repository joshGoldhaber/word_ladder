#!/bin/python3
from collections import deque



def word_ladder(start_word, end_word, dictionary_file='words5.dict'):
    '''
    Returns a list satisfying the following properties:

    1. the first element is `start_word`
    2. the last element is `end_word`
    3. elements at index i and i+1 are `_adjacent`
    4. all elements are entries in the `dictionary_file` file

    For example, running the command
    ```
    word_ladder('stone','money')
    ```
    may give the output
    ```
    ['stone', 'shone', 'phone', 'phony', 'peony', 'penny', 'benny', 'bonny', 'boney', 'money']
    ```
    but the possible outputs are not unique,
    so you may also get the output
    ```
    ['stone', 'shone', 'shote', 'shots', 'soots', 'hoots', 'hooty', 'hooey', 'honey', 'money']
    ```
    (We cannot use doctests here because the outputs are not unique.)

    Whenever it is impossible to generate a word ladder between the two words,
    the function returns `None`.

    HINT:
    See <https://github.com/mikeizbicki/cmc-csci046/issues/472> for a discussion about a common memory management bug that causes the generated word ladders to be too long in some cases.
    '''
    # a word is already a ladder to itself
    if start_word == end_word:
        return [start_word]

    with open(dictionary_file) as f:
        dictionary = f.read().split()

    stack = []
    stack.append(start_word)
    queue = deque()
    queue.append(stack)

    while queue:
        stack = queue.popleft()
        # loop over a copy so removing words below doesn't make the loop skip any
        for dict_word in dictionary.copy():
            if _adjacent(dict_word, stack[-1]):
                if dict_word == end_word:
                    return stack + [dict_word]
                stack_copy = stack.copy()
                stack_copy.append(dict_word)
                queue.append(stack_copy)
                dictionary.remove(dict_word)

    # the queue ran out without reaching end_word, so no ladder exists
    return None


'''
Create a stack
Push the start word onto the stack
Create a queue
Enqueue the stack onto the queue

While the queue is not empty
    Dequeue a stack from the queue
    For each word in the dictionary
        If the word is adjacent to the top of the stack
            If this word is the end word
                You are done!
                The front stack plus this word is your word ladder.
            Make a copy of the stack
            Push the found word onto the copy
            Enqueue the copy
            Delete word from the dictionary
'''

def verify_word_ladder(ladder):
    '''
    Returns True if each entry of the input list is adjacent to its neighbors;
    otherwise returns False.

    >>> verify_word_ladder(['stone', 'shone', 'phone', 'phony'])
    True
    >>> verify_word_ladder(['stone', 'shone', 'phony'])
    False
    '''
    # an empty ladder (or None) is not a valid ladder
    if not ladder:
        return False

    # compare each word with the word right after it
    for i in range(len(ladder) - 1):
        if not _adjacent(ladder[i], ladder[i + 1]):
            return False
    return True


def _adjacent(word1, word2):
    '''
    Returns True if the input words differ by only a single character;
    returns False otherwise.

    >>> _adjacent('phone','phony')
    True
    >>> _adjacent('stone','money')
    False
    '''
    if len(word1) == len(word2):
        num_matches = 0
        for i in range(len(word1)):
            if word1[i] == word2[i]:
                num_matches += 1
        if num_matches == len(word1)-1:
            return True
        else:
            return False
    # words of different lengths can never be adjacent
    return False