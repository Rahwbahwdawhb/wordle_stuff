from os import chdir
from os.path import dirname
from collections.abc import Iterable
from sys import argv
import importlib.resources as resources

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
        try:
            # Works when installed or run as module
            with resources.open_text("wordle_stuff.data_files", word_input) as f:
                words = f.read()
        except (ModuleNotFoundError, FileNotFoundError):
            from os.path import dirname,join,abspath
            # Fallback for running check.py directly
            here = dirname(__file__)
            data_path = join(here, "..", "data_files", word_input)
            with open(abspath(data_path)) as f:
                words = f.read()
        word_input=words.strip().split('\n')
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
    interactive_info_str=\
    """
    The command prompt can take up to 3 inputs (separated by -), which are:
    1. Spare/remaining letters, e.g arplo. This input is mandatory
    2. Correct indices and letters (green), e.g. for 1st letter being a and 3rd being o: 0a2o
    3. Letters that should be included (yellow), e.g. ao

    With these examples acceptable inputs are:
    arplo
    arplo-0a2o
    arplo--ao
    arplo-0a2o-ao

    To display this info again, enter ?
    To quit, enter !
    """
    print(interactive_info_str)
    while True:
        info_dict={'spare_letters':None,'correct_letters':[],'misplaced_letters':set()}
        input_str=input('Inputs: ').lower()
        if input_str=='!':
            break
        elif input_str=='?':
            print(interactive_info_str)
            continue
        try:
            check_bool=True
            for i, info in enumerate(input_str.split('-')):
                match i:
                    case 1:
                        if info!='':
                            if len(info)%2==0:
                                temp=[]
                                for ii in range(0,len(info),2):
                                    index=int(info[ii])
                                    if 0<=index<=4:
                                        if info[ii+1].isalpha():
                                            temp.append((index,info[ii+1]))
                                        else:
                                            print(f"{info[ii+1]} in {index}{info[ii+1]} for the 2nd input is not a letter")
                                            check_bool=False
                                            break
                                    else:
                                        print('Indices for the 2nd input has to be in the range [0,4]')
                                        check_bool=False
                                        break
                                info_dict['correct_letters']=temp
                            else:
                                print('The 2nd input has to have a length divisible by 2.')
                                check_bool=False
                                break
                    case _:
                        temp=set()
                        for c in info:
                            if c.isalpha():
                                temp.add(c)
                            else:
                                print(f"{c} in {info} is not a letter")
                                check_bool=False
                                break    
                match i:
                    case 0:
                        info_dict['spare_letters']=temp
                    case 2:
                        info_dict['misplaced_letters']=temp
            if check_bool:
                possible_word_count=0
                for word in word_set:
                    word_to_set={c for c in word}
                    if word_to_set.issubset(info_dict['spare_letters']) and info_dict['misplaced_letters'].issubset(word_to_set):
                        match_bool=True
                        for i,cl in info_dict['correct_letters']:
                            if word[i]!=cl:
                                match_bool=False
                        if match_bool:
                            possible_word_count+=1
                            print(word)
                print(f"{possible_word_count} possible words\n")
        except Exception as e:
            print(e)

def main():
    info_str=\
    """
    Initiate an inifinite loop that asks for spare input letters and outputs possible words.
    
    Running:
    check
    check wordle_words.txt

    uses a reference word list from the Wordle source code: https://github.com/tabatkins/wordle-list/blob/main/words
    
    Running:
    check words_alpha.txt

    uses a more extensive reference word list from: https://raw.githubusercontent.com/dwyl/english-words/refs/heads/master/words_alpha.txt
    """
    run_bool=True
    if len(argv) > 1:
        if argv[1] in ['h','-h','help','-help','--help']:
            print(info_str)
            run_bool=False
        else:
            word_file = argv[1]
    else:
        word_file = 'wordle_words.txt'
    if run_bool:
        interactive_letter_check(get_word_set(word_file))

if __name__=='__main__':
    main()