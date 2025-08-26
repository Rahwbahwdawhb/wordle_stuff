from os import chdir
from os.path import dirname
from collections.abc import Iterable

def get_word_set(word_input):
    """
    Function to generate a set of 5-letter words.
    
    Input:
    word_input = path to a file that contains words on separate rows,
                 or an iterable (e.g.) a list containig words

    Output:
    word_set = set of all 5-letter words from word_input
    """
    word_set=set()
    if isinstance(word_input,str):
        chdir(dirname(__file__))
        with open(word_input) as f:
            word_input=f.read().strip().split('\n')
    if isinstance(word_input,Iterable):
        for word in word_input:
            if len(word)!=5:
                    continue
            if isinstance(word,str):
                word_set.add(word.lower())
    else:
        print('Non-supported input type')
    return word_set

def interactive_letter_check(word_set):
    """
    Initiate an inifinite loop that asks for spare input letters and outputs possible words.

    Input:
    word_set = set of possible words
    """
    while True:
        letter_str=input('Enter spare letters without any separators (e.g. arplo) or ! to exit: ')
        if letter_str=='!':
            break
        spare_letters={c for c in letter_str.lower()}
        possible_word_count=0
        for word in word_set:
            if {c for c in word}.issubset(spare_letters):
                possible_word_count+=1
                print(word)
        print(f"{possible_word_count} possible words")
        print()

def main():
    interactive_letter_check(get_word_set('words_alpha.txt'))

if __name__=='__main__':
    main()