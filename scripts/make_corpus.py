import os
import pickle
import re

import pandas as pd

from spacy.lang.en import English

from tensorflow.keras.preprocessing.text import Tokenizer

CORPUS_DIRECTORY = '../corpus/dolly-parton'
OUTPUT_DIRECTORY = '../corpus'
META_DIRECTORY = '../metadata/'

FILES = [file for file in os.listdir(CORPUS_DIRECTORY) if file.startswith('dolly-parton_')]

NLP = English()

EXCLUDE_WORDS = ['Dolly Parton', 'Frank Daycus', 'Rachel Dennison', \
'Randy Parton', 'Jimmie Rodgers', 'Bill Owens', 'George Morgan', 'Ernie Ford', \
'O\'Hearn', 'Jean Ritchie', 'Music Pub Co.', 'verse', 'chorus', '©', \
 'copyright', 'Myra Brooks Welch', 'R E S P O N S I B I L I T Y']

TOKENIZER = Tokenizer()

def filter_lyrics(line):
    '''
    Marks lines containing stage directions like "[chorus]" or
    noting the names of the songwriter
    '''
    if '[' in line or any(word in line for word in EXCLUDE_WORDS) or line == [' ']:
        return False
    else:
        return True

def cap_repetition(line):
    '''
    Cap at 3x repetition of each word per line
    '''
    previous_word = []
    new_line = []
    rep = 0
    for i in line:
        if previous_word != i:
            rep = 0
            previous_word = i
            new_line.append(i)
        else:
            rep += 1
            if rep <= 2:
                new_line.append(i)
    return new_line

def clean_lyrics(raw):
    '''
    Text preprocessing
    1. Replace newlines with spaces
    2. lowercase everything
    3. tokenise into list of individual words
    '''
    doc = NLP(raw)
    lyrics = [token.orth_.lower() for token in doc if not token.is_punct]
    lyrics = [item for item in lyrics if item != ' ']
    return lyrics


if __name__ == "__main__":

    all_lyrics = []
    for file in FILES:
        with open(f'{CORPUS_DIRECTORY}/{file}') as f:
            raw = [line.strip() for line in f.read().split('\n') if filter_lyrics(line) and len(line) > 0]
            raw = ' '.join(raw)
            raw = re.sub(r'\\', '', raw)
            raw = re.sub(r'\.', '', raw)
            raw = re.sub(r'-', '', raw)
            raw = re.sub(r'"', '', raw)
            raw = re.sub('\?', '\'', raw)
            raw = re.sub('\s+', ' ', raw)
            lyrics = clean_lyrics(raw)
            capped = cap_repetition(lyrics)
            all_lyrics = all_lyrics + capped

    with open(f'{OUTPUT_DIRECTORY}/all_lyrics.txt', 'w') as f:
        f.write(' '.join(all_lyrics))

    seq_len = 61
    dolly_lines_x = []
    dolly_lines_y = []

    for i in range(seq_len, len(all_lyrics)):
        seq = all_lyrics[i:seq_len+i]
        if len(seq) == seq_len:
            dolly_lines_y.append(seq[-1])
            dolly_lines_x.append(seq[:-1])

    TOKENIZER.fit_on_texts(all_lyrics)

    sequences_x = TOKENIZER.texts_to_sequences(dolly_lines_x)
    sequences_y = TOKENIZER.texts_to_sequences(dolly_lines_y)

    NAMES = ['dolly_lines_x', 'dolly_lines_y', 'sequences_x', 'sequences_y']
    data = [dolly_lines_x, dolly_lines_y, sequences_x, sequences_y]

    name_data_dict = dict(zip(NAMES, data))

    for key, value in name_data_dict.items():
        new = pd.DataFrame(value)
        new.to_csv(f'{OUTPUT_DIRECTORY}/{key}.csv', index=False)

    with open(f'{META_DIRECTORY}tokenizer.pickle', 'wb') as handle:
        pickle.dump(TOKENIZER, handle, protocol=pickle.HIGHEST_PROTOCOL)
