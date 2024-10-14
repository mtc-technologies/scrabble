import argparse
import os
import sys

from collections import defaultdict
from pathlib import Path
from random import choice
from typing import Dict, List, Tuple

import requests


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
    with open(file_path, 'r') as file:
        for word in file:
            clean_word = word.strip()
            key = clean_word[0], len(clean_word)
            words[key].append(clean_word)
    return words


def download_word_list(url: str, destination: str) -> str:
    res = requests.get(url)
    # make sure we raise the error incase downloading failed
    res.raise_for_status()

    destination = Path(destination)

    if destination.is_dir():
        # combine the path with the file name derived as the last part of the URL
        # this makes a strong assumption that the url ends in a file name
        destination = destination / url.split("/")[-1]
    else:
        # ensure that in all instances the destination directory exists
        destination.parent.mkdir(parents=True, exist_ok=True)

    with open(destination, 'w') as file:
        file.write(res.text)

    return destination


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


def extract_app_parameters() -> Tuple:
    parser = argparse.ArgumentParser(description="Scramble words in a sentence using a word list.")
    parser.add_argument("--words-file", type=str, required=True, help="""
        Path to the file containing words. This can be a URL or a local file system.
        If it's a url, the file will downloaded on first run and saved locally for future runs.
        If it's a path to file, the file will be loaded and used
    """)
    parser.add_argument("--sentence", type=str, help="The sentence to be scrambled.", required=True)
    parser.add_argument("--force-download", help="The sentence to be scrambled. Defaults to True", action='store_true')
    parser.add_argument("--download-dest", type=str, help="The sentence to be scrambled.", required=False)

    args = parser.parse_args()

    words_file = args.words_file
    original_sentence = args.sentence

    # check if we passed a url and need to download the file
    if args.words_file.startswith("http"):
        filename = os.path.basename(args.words_file)
        # use current working dir if no download path specified
        download_path = args.download_dest or os.getcwd()
        filepath = Path(download_path) / filename

        # if we forcing download or the file does not exists, download
        if args.force_download or not filepath.exists():
            print(f"Fetching words file from: {words_file}")
            download_word_list(words_file, filepath)
            print(f"Word list save a: {filepath}")
    else:
        filepath = Path(args.words_file)
        assert filepath.exists(), "The specified local words file does not exist."

    return filepath, original_sentence


if __name__ == "__main__":
    destination_filename, original_sentence = extract_app_parameters()
    word_list = read_word_list(destination_filename)
    scrabled_sentence = scrable_sentence(original_sentence, word_list)

    print(f"Original sentence: {original_sentence}")
    print(f"Scrambled sentence: {scrabled_sentence}")
