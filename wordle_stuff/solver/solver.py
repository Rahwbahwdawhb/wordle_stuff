#fixa så kan spela mot sig själv
#script för att benchmarka poängsättning

#snabba upp bortfiltrering av felaktiga ord
#..blev mkt långsammare när lade till:
# try:
#     self.letter_word_dict[_position[1]].remove(_word)
# except KeyError:
#     pass
#i correct_for_invalid_letters

#kolla närmare på hur nuvarande poäng sätts
#implementera alternativ strategi där väljer ord mest olikt 1a föreslagna ord

import importlib.resources as resources
from os.path import dirname,join,abspath
from sys import argv

def get_dicts(word_file="wordle_words.txt"):
    """
    Read a file that contains a list of words (one word per row) and create a four
    dictionaries to establish relations between them.

    Inputs:
    word_file_module = location of module that contains the word data file
    word_file = the name of the word file
    Outputs:
    position_word_dict = dictionary with (letter_index,letter) as keys and words that contains
                         the letter at the letter_index position
    word_position_dict = dictionary with words as keys and (letter_index,letter) as values
                         ("inverse" of position_word_dict)
    letter_word_dict = dictionary with letters as keys and words (that contain the letter for
                       for a given key)
    word_unique_character_dict = dictionary with words as keys and the number of unique
                                 characters those words contain as values
    """
    
    position_word_dict=dict()
    word_position_dict=dict()
    letter_word_dict=dict()
    word_unique_character_dict=dict()
    try:
        # Works when installed or run as module
        with resources.open_text("wordle_stuff.data_files", word_file) as f:
            words = f.read()
    except (ModuleNotFoundError, FileNotFoundError):
        # Fallback for running check.py directly
        here = dirname(__file__)
        data_path = join(here, "..", "data_files", word_file)
        with open(abspath(data_path)) as f:
            words = f.read()
    finally:
        for word in words.strip().split('\n'):        
            if len(word)!=5:
                continue
            temp_set=set()
            for i,ch in enumerate(word):
                temp_set.add(ch)
                try:
                    position_word_dict[(i,ch)].add(word)                    
                except KeyError:
                    position_word_dict[(i,ch)]={word}
                try:
                    word_position_dict[word].add((i,ch))
                except KeyError:
                    word_position_dict[word]={(i,ch)}
                try:
                    letter_word_dict[ch].add(word)
                except KeyError:
                    letter_word_dict[ch]={word}
            word_unique_character_dict[word]=len(temp_set)
    return position_word_dict,word_position_dict,letter_word_dict,word_unique_character_dict

def strategy(word_position_dict,letter_word_dict,word_unique_character_dict,position_word_dict):
    vowels={'a','e','i','o','u','y'}
    vowel_guesses=[]
    vowel_count=0
    for word in word_position_dict.keys():
        vowel_sum=0
        for c in word:
            if c in vowels:
                if word.count(c)==1:
                    vowel_sum+=2
                else:
                    vowel_sum+=1
        if vowel_count<vowel_sum:
            vowel_guesses=[word]
            vowel_count=vowel_sum
        elif vowel_count==vowel_sum:
            vowel_guesses.append(word)
    letter_word_guesses=[]
    letter_word_count=0
    for word in vowel_guesses:
        letter_sum=0
        for c in word:
            letter_sum+=len(letter_word_dict[c])
        if letter_word_count<letter_sum:
            letter_word_guesses=[word]
            letter_word_count=letter_sum
        elif letter_word_count==letter_sum:
            letter_word_guesses.append(word)
    # for word in word_position_dict.keys():
    #     vowel_sum=0
    #     for c in word:
    #         if c in vowels:
    #             vowel_sum+=1
    #     if vowel_count<vowel_sum:
    #         vowel_guesses=[word]
    #         vowel_count=vowel_sum
    #     elif vowel_count==vowel_sum:
    #         vowel_guesses.append(word)
    unique_guesses=[]
    unique_count=0
    for word in word_position_dict.keys():
        if unique_count<word_unique_character_dict[word]:
            unique_guesses=[word]
            unique_count=word_unique_character_dict[word]
        elif unique_count==word_unique_character_dict[word]:
            unique_guesses.append(word)
    # next_guess=unique_guesses[0] if unique_guesses else ''
    position_guesses=[]
    position_count=0
    for word in unique_guesses:
        position_sum=0
        for position in word_position_dict[word]:
            position_sum+=len(position_word_dict[position])-1
        if position_count<position_sum:
            position_guesses=[word]
            position_count=position_sum
        elif position_count==position_sum:
            position_guesses.append(word)
    next_guess=position_guesses[0] if position_guesses else ''

        # next_guess=''
        # reference_word_point=0
        # reference_letter_count=0
        # for word,positions in word_position_dict.items():
        #     position_count=0
        #     letter_count=0
        #     for position in positions:
        #         position_count+=len(position_word_dict[position])-1
        #         letter_count+=len(letter_word_dict[position[1]])
        #     word_point=position_count*word_unique_character_dict[word]
        #     if reference_word_point<word_point:
        #         next_guess=word
        #         reference_word_point=word_point
        #         reference_letter_count=letter_count
        #     elif reference_word_point==word_point:
        #         if reference_letter_count<letter_count:
        #             next_guess=word
        #             reference_letter_count=letter_count
        #         elif reference_letter_count==letter_count:
        #             next_guess+=f",{word}"
    return next_guess

class guess_suggester:
    def __init__(self,word_file="wordle_words.txt"):
        self.word_file=word_file
        self.initialize()
    def initialize(self):
        self.position_word_dict,\
        self.word_position_dict,\
        self.letter_word_dict,\
        self.word_unique_character_dict=get_dicts(self.word_file)
        self.invalid_letters=set()
        self.correct_letters=set()
        self.present_letters=set()
        self.correct_letter_count_dict=dict()
    def suggest_guess(self,strategy_for_next_guess=strategy):
        """
        
        """
        # update current:
        # self.position_word_dict
        # self.word_position_dict
        # self.letter_word_dict
        # self.word_unique_character_dict
        # based on contents in:
        # self.correct_letters
        # self.present_letters
        # self.invalid_letters  
        if self.correct_letters:
            corrected_position_word_dict=dict()
            corrected_word_position_dict=dict()
            corrected_letter_word_dict=dict()
            corrected_word_unique_character_dict=dict()
            valid_words_set=set()
            for position in self.correct_letters:
                if len(valid_words_set)==0:
                    valid_words_set=self.position_word_dict[position]
                else:
                    valid_words_set=valid_words_set.intersection(self.position_word_dict[position])
            for word in valid_words_set:
                corrected_word_position_dict[word]=self.word_position_dict[word]
                corrected_word_unique_character_dict[word]=self.word_unique_character_dict[word]
                for position in self.word_position_dict[word]:
                    try:
                        corrected_position_word_dict[position].add(word)
                    except KeyError:
                        corrected_position_word_dict[position]={word}
                    try:
                        corrected_letter_word_dict[position[1]].add(word)
                    except KeyError:
                        corrected_letter_word_dict[position[1]]={word}
            self.word_position_dict=corrected_word_position_dict
            self.position_word_dict=corrected_position_word_dict
            self.word_unique_character_dict=corrected_word_unique_character_dict
            self.letter_word_dict=corrected_letter_word_dict
        if self.present_letters:
            corrected_position_word_dict=dict()
            corrected_word_position_dict=dict()
            corrected_letter_word_dict=dict()
            corrected_word_unique_character_dict=dict()
            valid_words_set=set()
            for letter in self.present_letters:
                if len(valid_words_set)==0:
                    valid_words_set=self.letter_word_dict[letter]
                else:
                    valid_words_set=valid_words_set.intersection(self.letter_word_dict[letter])
            for word in valid_words_set:
                corrected_word_position_dict[word]=self.word_position_dict[word]
                corrected_word_unique_character_dict[word]=self.word_unique_character_dict[word]
                for position in self.word_position_dict[word]:
                    try:
                        corrected_position_word_dict[position].add(word)
                    except KeyError:
                        corrected_position_word_dict[position]={word}
                    try:
                        corrected_letter_word_dict[position[1]].add(word)
                    except KeyError:
                        corrected_letter_word_dict[position[1]]={word}
            self.word_position_dict=corrected_word_position_dict
            self.position_word_dict=corrected_position_word_dict
            self.word_unique_character_dict=corrected_word_unique_character_dict
            self.letter_word_dict=corrected_letter_word_dict

        for ch in self.invalid_letters:
            if ch in self.correct_letter_count_dict: #handling case where a letter appears in the word but no more times than what's already identified
                words_to_remove=[]
                for word in self.word_position_dict.keys():
                    if ch in word and word.count(ch)>self.correct_letter_count_dict[ch]:
                        words_to_remove.append(word)
                self.correct_for_invalid_letters(words_to_remove,ch,multiple_occurrence_removal_bool=True)
            else:
                try:
                    words_to_remove=set(self.letter_word_dict[ch])
                    self.correct_for_invalid_letters(words_to_remove,ch)
                except KeyError: #if the letter corresponding to ch has already been deleted
                    continue
        # apply strategy to suggest a new guess
        next_guess=strategy_for_next_guess(self.word_position_dict,self.letter_word_dict,self.word_unique_character_dict,self.position_word_dict)
        # self.vowels={'a','e','i','o','u','y'}
        # vowel_guesses=[]
        # vowel_count=0
        # for word in self.word_position_dict.keys():
        #     vowel_sum=0
        #     for c in word:
        #         if c in self.vowels:
        #             if word.count(c)==1:
        #                 vowel_sum+=2
        #             else:
        #                 vowel_sum+=1
        #     if vowel_count<vowel_sum:
        #         vowel_guesses=[word]
        #         vowel_count=vowel_sum
        #     elif vowel_count==vowel_sum:
        #         vowel_guesses.append(word)
        # letter_word_guesses=[]
        # letter_word_count=0
        # for word in vowel_guesses:
        #     letter_sum=0
        #     for c in word:
        #         letter_sum+=len(self.letter_word_dict[c])
        #     if letter_word_count<letter_sum:
        #         letter_word_guesses=[word]
        #         letter_word_count=letter_sum
        #     elif letter_word_count==letter_sum:
        #         letter_word_guesses.append(word)
        # # for word in self.word_position_dict.keys():
        # #     vowel_sum=0
        # #     for c in word:
        # #         if c in self.vowels:
        # #             vowel_sum+=1
        # #     if vowel_count<vowel_sum:
        # #         vowel_guesses=[word]
        # #         vowel_count=vowel_sum
        # #     elif vowel_count==vowel_sum:
        # #         vowel_guesses.append(word)
        # unique_guesses=[]
        # unique_count=0
        # for word in self.word_position_dict.keys():
        #     if unique_count<self.word_unique_character_dict[word]:
        #         unique_guesses=[word]
        #         unique_count=self.word_unique_character_dict[word]
        #     elif unique_count==self.word_unique_character_dict[word]:
        #         unique_guesses.append(word)
        # # next_guess=unique_guesses[0] if unique_guesses else ''
        # position_guesses=[]
        # position_count=0
        # for word in unique_guesses:
        #     position_sum=0
        #     for position in self.word_position_dict[word]:
        #         position_sum+=len(self.position_word_dict[position])-1
        #     if position_count<position_sum:
        #         position_guesses=[word]
        #         position_count=position_sum
        #     elif position_count==position_sum:
        #         position_guesses.append(word)
        # next_guess=position_guesses[0] if position_guesses else ''

        # # next_guess=''
        # # reference_word_point=0
        # # reference_letter_count=0
        # # for word,positions in self.word_position_dict.items():
        # #     position_count=0
        # #     letter_count=0
        # #     for position in positions:
        # #         position_count+=len(self.position_word_dict[position])-1
        # #         letter_count+=len(self.letter_word_dict[position[1]])
        # #     word_point=position_count*self.word_unique_character_dict[word]
        # #     if reference_word_point<word_point:
        # #         next_guess=word
        # #         reference_word_point=word_point
        # #         reference_letter_count=letter_count
        # #     elif reference_word_point==word_point:
        # #         if reference_letter_count<letter_count:
        # #             next_guess=word
        # #             reference_letter_count=letter_count
        # #         elif reference_letter_count==letter_count:
        # #             next_guess+=f",{word}"
        return next_guess
    def correct_for_invalid_letters(self,words_to_remove,ch,multiple_occurrence_removal_bool=False):
        wr=[w for w in words_to_remove]
        while words_to_remove:
            word_to_remove=words_to_remove.pop()
            try:
                positions_to_remove=[_position for _position in self.word_position_dict[word_to_remove] if _position[1]==ch]
            except KeyError:
                continue
            for position in positions_to_remove:
                try:
                    self.letter_word_dict[position[1]].remove(word_to_remove)
                except KeyError:
                    pass
                try:
                    for _word in list(self.position_word_dict[position]):
                        # for multiple_occurrence_removal, all words to be removed are provided in the words_to_remove input
                        # go to next iteration if _word is not in words_to_remove and is not word_to_remove (the current word
                        # that is to be removed)
                        if multiple_occurrence_removal_bool and _word not in words_to_remove and _word!=word_to_remove:
                            continue
                        self.position_word_dict[position].remove(_word)
                        for _position in list(self.word_position_dict[_word]):
                            try:
                                self.position_word_dict[_position].remove(_word)
                            except KeyError:
                                pass
                            try:
                                self.letter_word_dict[_position[1]].remove(_word)
                            except KeyError:
                                pass
                    # for multiple_occurrence_removal, positions are still valid (for words not having more
                    # letter occurrences than what's allowed)
                    # for non multiple_occurrence_removal, all positions (and their associated words) that contain
                    # the letter to be removed must be removed
                    if not multiple_occurrence_removal_bool:
                        del self.position_word_dict[position]
                except KeyError:
                    pass
            for k,v in self.letter_word_dict.items():
                for _v in v:
                    if _v not in self.word_position_dict:
                        print(k,_v,_v in wr)
                        1
            del self.word_position_dict[word_to_remove]
        # for multiple_occurrence_removal, the letter with multiple occurrences is still valid
        # (for words not having more letter occurrences than what's allowed)
        # for non multiple_occurrence_removal, all words associated with the letter to be removed 
        # must be removed
        if not multiple_occurrence_removal_bool:
            del self.letter_word_dict[ch]
    def interactive_guessing(self):
        info_str=\
        """
        This is an interactive guess suggestion prompt, enter:
        incorrect_letters,letter_index1Letter1letter_index2Letter2,present_letters
        e.g. for incorrect letters: abc, and correct letters
            1st r 5th y, and present letters uv enter:
        abc,0r4y,uv

        Special inputs:
        ?   Show this message again
        !   Quit
        -   Restart (incorrect and correct letters are disregarded)
        """
        print(info_str)
        while True:
            next_guess=self.suggest_guess()
            if next_guess:
                print(f"Suggested guess: {next_guess}\n")
            else:
                print('Out of words, enter - to restart.')
            input_str=input('Input: ')
            if input_str=='?':
                print(info_str)
                continue
            elif input_str=='!':
                break
            elif input_str=='-':
                self.initialize()
                continue
            input_list=input_str.split(',')
            match len(input_list):
                case 1:
                    new_correct_letters=set()
                    new_present_letters=set()
                case 2:
                    new_correct_letters={(int(input_list[1][i]),input_list[1][i+1]) for i in range(0,len(input_list[1]),2)}
                    new_present_letters=set()
                case 3:
                    new_correct_letters={(int(input_list[1][i]),input_list[1][i+1]) for i in range(0,len(input_list[1]),2)}
                    new_present_letters={ch.lower() for ch in input_list[2] if ch.isalpha()}
            self.invalid_letters=self.invalid_letters.union({ch.lower() for ch in input_list[0] if ch.isalpha()})
            for position in new_correct_letters:
                if position not in self.correct_letters:
                    self.correct_letters.add(position)
                    try:
                        self.correct_letter_count_dict[position[1]]+=1
                    except KeyError:
                        self.correct_letter_count_dict[position[1]]=1
            self.correct_letters=self.correct_letters.union(new_correct_letters)
            self.present_letters=self.present_letters.union(new_present_letters)

def main():
    info_str=\
    """
    Analyze the word content in a given file containig a list of words (one per row).
    
    Running:
    analyze
    analyze wordle_words.txt

    uses a reference word list from the Wordle source code: https://github.com/tabatkins/wordle-list/blob/main/words
    
    Running:
    analyze words_alpha.txt

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
        gs=guess_suggester(word_file=word_file)
        gs.interactive_guessing()
if __name__=='__main__':
    main()