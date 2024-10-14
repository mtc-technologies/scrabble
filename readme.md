# Scrabble
Simple program for scrabbling sentences based on word length and first character match


## Running the Application

### Requirements
- **Python 3.11+** (This was tested using this version; it should work from 3.8+)

---

### v1 - Basic
This version requires that the words list is pre-downloaded and saved somewhere in the file system. To run the first version of the application, follow the instructions below.

#### Checkout the Correct Version Tag
```shell
git checkout v1-buddled-word-list
```

#### To Get the List of Options Available
```shell
python3 main.py --help
```

#### Run the Application
```shell
python3 main.py --words-file PATH_TO_WORDS_FILE --sentence SENTENCE
```

### Example Run
```bash
python3 main.py --words-file words_alpha.txt --sentence "likable frier frog arm delegated"
```

---

### v2 - Download and Cacheable Words List
This version can read a words list file from a path or download the file from a given URL. To run this version of the application, follow the instructions below.

#### Checkout the Correct Version Tag
```shell
git checkout v2-downloadable-and-cacheable-wordlist && pip install -r requirements.txt
```

#### To Get the List of Options Available
```shell
python3 main.py --help
```

#### Run the Application
```shell
python3 main.py --words-file PATH_TO_WORDS_FILE --sentence SENTENCE
```

### Example Run
```bash
python3 main.py --words-file https://raw.githubusercontent.com/dwyl/english-words/refs/heads/master/words_alpha.txt --sentence "likable frier frog arm delegated" --force-download --download-dest tmp
```

---

### v3 - Latest Version with Caching of Pre-Processed Words List Data Structure
In this version, we improve the performance of the application by caching the words list processing output, so subsequent runs don't need to do the computation again. To run this version of the application, follow the instructions below.

#### Checkout the Correct Version Tag
```shell
git checkout v3-cacheable-preprocessed-word-list && pip install -r requirements.txt
```

#### To Get the List of Options Available
```shell
python3 main.py --help
```

#### Run the Application
```shell
python3 main.py --words-file PATH_TO_WORDS_FILE --sentence SENTENCE
```

### Example Run
```bash
python3 main.py --words-file https://raw.githubusercontent.com/dwyl/english-words/refs/heads/master/words_alpha.txt --sentence "likable frier frog arm delegated" --use-cache
```

---
