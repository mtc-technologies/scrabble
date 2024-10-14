import argparse
import os
import pickle
import sys

from collections import defaultdict
from pathlib import Path
from random import choice
from typing import Dict, List, Tuple

import requests


def read_words_from_cache(cache_file: str) -> Dict[Tuple[str, int], List[str]]:
    try:
        with open(cache_file, 'rb') as file:
            return pickle.load(file)
    except:
        # TODO: handle specific errors instead of supressing them
        return None

def save_words_to_cache(cache_file: Path, words: Dict[Tuple[str, int], List[str]]):
    try:
        with open(cache_file, 'wb') as cache:
            pickle.dump(words, cache)
    except:
        return False


def get_cache_file(destination: Path) -> Path:
    """
    So I want to cache the pre computed dict of words as an object so that next
    time I dont have to re compute them
    """
    parent_dir = destination.parent
    cache_dir = parent_dir / '.cache'

    # Ensure the cache dir exists
    cache_dir.mkdir(parents=True, exist_ok=True)

    return cache_dir / f"{destination.stem}.pkl"


def read_word_list(file_path: str, use_cache=True) -> Dict[Tuple[str, int], List[str]]:
    # initialise a dict with each item initialised as an empty list to avoid
    # having to check and create a new list before appending
    words = defaultdict(list)

    # If we are allowed to use cache and we have cache data, use it
    if use_cache and (cache_words := read_words_from_cache(get_cache_file(file_path))):
        print("Using cache pre-computed datastructure\n")
        return cache_words

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

    if use_cache:
        save_words_to_cache(get_cache_file(file_path), words)

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


def scrablle_sentence(sentence: str, words: Dict[Tuple[str, int], List[str]]) -> str:
    """
    scrablles the sentence using the supplied word list
    """
    scrablled_sentence_words = [swap_word(word, words) for word in sentence.split()]
    return " ".join(scrablled_sentence_words)


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
    parser.add_argument("--use-cache", action='store_true', help="""
        If we should use cache.
        This is because the words file does not cache that often and we can save
        the pre computed results so next time we dont need to re computed the datastructure.
        This is overriden by --force-download, if we downloading, we wont use cache
    """)

    args = parser.parse_args()

    words_file = args.words_file
    original_sentence = args.sentence
    use_cache = args.use_cache and not args.force_download

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
        assert filepath.exists(), "No words file specified or the specified local words file does not exist."

    return filepath, original_sentence, use_cache


if __name__ == "__main__":
    destination_filename, original_sentence, use_cache = extract_app_parameters()
    word_list = read_word_list(destination_filename, use_cache)
    scrablled_sentence = scrablle_sentence(original_sentence, word_list)

    print(f"\nOriginal sentence: {original_sentence}")
    print(f"Scrambled sentence: {scrablled_sentence}")
