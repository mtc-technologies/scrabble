import argparse
import sys

from collections import defaultdict
from pathlib import Path
from random import choice
from typing import Dict, List, Tuple


def read_word_list(file_path: str) -> Dict[Tuple[str, int], List[str]]:
    # initialise a dict with each item initialised as an empty list to avoid
    # having to check and create a new list before appending
    words = defaultdict(list)

    """
    scan through the file and load the words into the dict.
    the structure with be as per below where the key is a 2 item tuple with
    first item being the starting letter and the second being the length of the
    words matching that bucket:
        {
            ('a', 2): ['aa', 'ab'],
            ('a', 5): ['asdgs', 'arfte']
            ...
        }
    """
    with open(file_path) as file:
        for word in file:
            clean_word = word.strip()
            key = clean_word[0], len(clean_word)
            words[key].append(clean_word)
    return words


def swap_word(word: str, words: Dict[Tuple[str, int], List[str]]) -> str:
    """
    swaps the word with a matching one in the supplied list of words
    """
    key = (word[0], len(word)) # The key to the words is a tupple
    replacements = words.get(key, [])

    # randomly select a word from the possible list matching first char and length
    if replacements:
        return choice(replacements)

    # If there was not suitable replacements, return the original word
    return word


def scrable_sentence(sentence: str, words: Dict[Tuple[str, int], List[str]]) -> str:
    """
    scrables the sentence using the supplied word list
    """
    scrabled_sentence_words = [swap_word(word, words) for word in sentence.split()]
    return " ".join(scrabled_sentence_words)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scramble words in a sentence using a word list.")
    parser.add_argument("--words-file", type=str, required=True, help="""
        Path to the file containing words. This can be a URL or a local file system.
        If it's a url, the file will downloaded on first run and saved locally for future runs.
        If it's a path to file, the file will be loaded and used
    """)
    parser.add_argument("--sentence", type=str, help="The sentence to be scrambled.", required=True)

    args = parser.parse_args()

    words_file = args.words_file
    original_sentence = args.sentence

    word_list = read_word_list(words_file)
    scrabled_sentence = scrable_sentence(original_sentence, word_list)

    print(f"Original sentence: {original_sentence}")
    print(f"Scrambled sentence: {scrabled_sentence}")
