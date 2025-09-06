import importlib.resources as resources
from os.path import dirname,join,abspath
from time import perf_counter

try:
    from solver_strategies import implement_strategy
except ModuleNotFoundError:
    1

class letter:
    def __init__(self,character):
        self.character=character
        self.in_words_set=set()
        self.occurrence_dict=dict() #keys=number of times the letter appears, values=words in which the letter appears that many times
        self.positions_dict=dict()
        self.in_answer_bool=False
        self.potential_words_set=set()
    def add_word(self,word,occurrences,positions,prep_bool=True):
        self.in_words_set.add(word)
        self.occurrence_dict.setdefault(occurrences,{word}).add(word)
        for position in positions:
            self.positions_dict.setdefault(position,{word}).add(word)
        if prep_bool:
            self.potential_words_set.add(word)
    def prep_for_search(self):
        self.in_answer_bool=False
        self.potential_words_set={word for word in self.in_words_set}

class filter_handler:
    def __init__(self,word_file="wordle_words.txt"):
        self.letters_dict=dict()
        self.potential_letters_dict=dict()
        self.present_letters_count_dict=dict()
        self.correct_letters_count_set=set()
        for ch in range(ord('a'), ord('z') + 1):
            _letter=letter(chr(ch))
            _letter.prep_for_search()
            self.letters_dict[chr(ch)]=_letter
            self.potential_letters_dict[chr(ch)]=_letter
            self.present_letters_count_dict[chr(ch)]=0
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
            self.possible_wordle_words_set=set()
            self.wordle_words_dict=dict()
            self.unique_letters_dict=dict()

            self.overall_word_position_dict=dict() #new, for single loop filtering
            self.overall_word_letter_dict=dict() #new, for single loop filtering
            for word in words.strip().split('\n'):        
                if len(word)!=5:
                    continue
                self.possible_wordle_words_set.add(word)

                #counting occurrences outside of the letter add_word-function
                #to only loop once through the word, and not once for each character
                temp_count_dict=dict()
                temp_position_dict=dict()
                self.overall_word_position_dict[word]=set() #new, for single loop filtering
                for i,ch in enumerate(word):
                    temp_count_dict[ch]=temp_count_dict.get(ch, 0)+1
                    temp_position_dict.setdefault(ch,{i}).add(i)
                    self.overall_word_position_dict[word].add((i,ch)) #new, for single loop filtering
                self.unique_letters_dict[word]=len(temp_count_dict)
                self.overall_word_letter_dict[word]=temp_count_dict #new, for single loop filtering
                for ch,count in temp_count_dict.items():
                    self.letters_dict[ch].add_word(word,count,temp_position_dict[ch])
                    self.wordle_words_dict.setdefault(word,{ch}).add(ch)
    def reset(self):
        self.possible_wordle_words_set=set(self.wordle_words_dict.keys())
        for ch,_letter in self.letters_dict.items():
            _letter.prep_for_search()
            self.potential_letters_dict[ch]=_letter
            self.present_letters_count_dict[ch]=0
        self.correct_letters_count_set=set()
    def handle_present_letters(self,present_letters,sync_potential_letter_dicts_bool=False):
        if present_letters:
            present_letters_ch=set()
            blocked_positions=set()
            for position,ch in present_letters:
                present_letters_ch.add(ch)
                blocked_positions.add((position,ch))
            N_letters_ch=len(present_letters_ch)
            for word in list(self.possible_wordle_words_set):
                temp_check_dict=dict()
                ok_1=True
                ok_2=True
                for i,ch in enumerate(word):
                    if (i,ch) in blocked_positions:
                        ok_1=False
                        break
                    if ch in present_letters_ch:
                        temp_check_dict[ch]=True
                
                if len(temp_check_dict)!=N_letters_ch:
                    ok_2=False
                if not (ok_1 and ok_2):
                    self.possible_wordle_words_set.remove(word)
            if sync_potential_letter_dicts_bool:
                self.sync_potential_letter_dicts()
    def handle_correct_letters(self,correct_letters,sync_potential_letter_dicts_bool=False):
        temp_count_dict=dict()
        for position,ch in correct_letters:
            self.correct_letters_count_set.add((position,ch))
            ref_set=self.potential_letters_dict[ch].positions_dict[position]
            self.potential_letters_dict[ch].in_answer_bool=True
            temp_count_dict[ch]=temp_count_dict.get(ch,0)+1
            self.possible_wordle_words_set=self.possible_wordle_words_set.intersection(ref_set)
        for ch,temp_count in temp_count_dict.items():
            self.present_letters_count_dict[ch]=max(self.present_letters_count_dict[ch],temp_count)
        if sync_potential_letter_dicts_bool:
            self.sync_potential_letter_dicts()
    def handle_invalid_letters(self,invalid_letters,sync_potential_letter_dicts_bool=False):
        for ch in invalid_letters:
            try:
                _letter=self.potential_letters_dict[ch]
            except KeyError: #if guess includes invalid letter already deleted from previous guess
                continue
            if _letter.in_answer_bool:
                for occurrence,words in _letter.occurrence_dict.items():
                    if self.present_letters_count_dict[ch]<occurrence:
                        for word in words:
                            try:
                                _letter.potential_words_set.remove(word)
                            except KeyError:
                                pass
                            try:
                                self.possible_wordle_words_set.remove(word)
                            except KeyError:
                                pass
            else:
                for word in list(_letter.potential_words_set):
                    try:
                        self.possible_wordle_words_set.remove(word)
                    except KeyError:
                        pass
                    _letter.potential_words_set.remove(word)
                del self.potential_letters_dict[ch]
        if sync_potential_letter_dicts_bool:
            self.sync_potential_letter_dicts()
    def sync_potential_letter_dicts(self):
        for ch,_letter in self.potential_letters_dict.items():
            _letter.potential_words_set=_letter.potential_words_set.intersection(self.possible_wordle_words_set)
    # def debug(self):
    #     if 'tower' not in self.possible_wordle_words_set:
    #         1
    def handle_input_letters(self,invalid_letters,new_present_letters_set,new_present_letters_dict,correct_letters,sync_potential_letter_dicts_bool=False):
        temp_count_dict=dict()
        for position_ch in  correct_letters:
            self.correct_letters_count_set.add(position_ch)
            self.potential_letters_dict[position_ch[1]].in_answer_bool=True
            temp_count_dict[position_ch[1]]=temp_count_dict.get(position_ch[1],0)+1
        for ch,temp_count in temp_count_dict.items():
            self.present_letters_count_dict[ch]=max(self.present_letters_count_dict[ch],temp_count)
        # present_letters_ch_dict=dict()
        for _,ch in new_present_letters_set:
            # present_letters_ch_dict[ch]=present_letters_ch_dict.get(ch,0)+1
            self.potential_letters_dict[ch].in_answer_bool=True
        
        for word in list(self.possible_wordle_words_set):
            if correct_letters:
                word_removed_bool=False
                for position_ch in correct_letters:
                    if position_ch not in self.overall_word_position_dict[word]:
                        self.possible_wordle_words_set.remove(word)
                        word_removed_bool=True
                        break
                if word_removed_bool:
                    continue
            if new_present_letters_set:
                word_removed_bool=False
                for position_ch in new_present_letters_set:
                    #present letter=letter that should be in the word but not at the guessed position
                    #remove all words with the letter in the guessed position
                    if position_ch in self.overall_word_position_dict[word]:
                        self.possible_wordle_words_set.remove(word)
                        word_removed_bool=True
                        break
                    else:
                        #remove all words that don't contain all of the new present letters
                        #if one would pass in all encountered present letters (not just new ones)
                        #the entire possible word set would get empty since the words that are present
                        #are those that did not have 
                        for ch,count in new_present_letters_dict.items():
                            if ch not in self.overall_word_letter_dict[word] or self.overall_word_letter_dict[word][ch]<count:
                                self.possible_wordle_words_set.remove(word)
                                word_removed_bool=True
                                break
                        if word_removed_bool:
                            break
                if word_removed_bool:
                    continue
            if invalid_letters:
                for ch in invalid_letters:
                    if ch in word:
                        if self.letters_dict[ch].in_answer_bool:
                            if self.overall_word_letter_dict[word][ch]<self.present_letters_count_dict[ch]:
                                self.possible_wordle_words_set.remove(word)
                        else:
                            try:
                                self.possible_wordle_words_set.remove(word)
                            except KeyError:
                                pass
                            try:
                                del self.potential_letters_dict[ch]
                            except KeyError:
                                pass

class game_handler:
    def __init__(self,_filter_handler):
        self._filter_handler=_filter_handler
    def parse_target_word(self,target_word):
        self.target_word_position_set=set()
        self.target_word_letter_count_dict=dict()
        for i,ch in enumerate(target_word):
            self.target_word_position_set.add((i,ch))
            self.target_word_letter_count_dict[ch]=self.target_word_letter_count_dict.get(ch,0)+1
    def evaluate_word(self,word):
        correct_letters=set()
        correct_letters_count=dict()
        present_letters=set()
        incorrect_letters=set()
        temp_count_dict=dict()
        for i,ch in enumerate(word):
            if (i,ch) in self.target_word_position_set:
                correct_letters.add((i,ch))
                correct_letters_count[ch]=correct_letters_count.get(ch,0)+1
            elif ch in self.target_word_letter_count_dict:
                temp=temp_count_dict.get(ch,0)
                if temp<self.target_word_letter_count_dict[ch]:
                    present_letters.add((i,ch))
                    temp_count_dict[ch]=temp+1
            else:
                incorrect_letters.add(ch)
        verified_present_letters=set()
        for i,ch in present_letters:
            if ch in correct_letters_count and correct_letters_count[ch]==self.target_word_letter_count_dict[ch]:
                incorrect_letters.add(ch)
            else:
                verified_present_letters.add((i,ch))
        return incorrect_letters,correct_letters,verified_present_letters
    def evaluate_word_2(self,word):
        #count correct letters (appear in the right positions) and present letters
        #(appear in the word but in different positions)
        correct_letters_count=dict()
        new_present_letters=set()
        temp_count_dict=dict()
        for i,ch in enumerate(word):
            if (i,ch) in self.target_word_position_set:
                self.correct_letters_set.add((i,ch))
                correct_letters_count[ch]=correct_letters_count.get(ch,0)+1
            elif ch in self.target_word_letter_count_dict:
                temp=temp_count_dict.get(ch,0)
                if temp<self.target_word_letter_count_dict[ch]:
                    new_present_letters.add((i,ch))
                    temp_count_dict[ch]=temp+1
            else:
                self.invalid_letters_set.add(ch)
        #when all correct letters have been counted, check if the number of present letters
        #would make a letter appear more than the correct number of times, and if so mark it as invalid
        #otherwise, mark them as verified up until the number of them exceeds the correct number of times
        #they should appear
        verified_present_letters_dict=dict()
        for i,ch in new_present_letters:
            if ch in correct_letters_count and correct_letters_count[ch]==self.target_word_letter_count_dict[ch]:
                self.invalid_letters_set.add(ch)
            else:
                self.present_letters_set.add((i,ch))
                verified_present_letters_dict[ch]=verified_present_letters_dict.get(ch,0)+1
        return verified_present_letters_dict

    def start_noninteractive_game(self,game_strategy,target_word=None,verbose_bool=False):
        self._filter_handler.reset()
        all_possible_words=set(self._filter_handler.wordle_words_dict.keys())
        if not target_word:
            target_word=next(iter(self._filter_handler.possible_wordle_words_set))
        self.parse_target_word(target_word)
        invalid_letters_set=set()
        present_letters_set=set()
        self.invalid_letters_set=set()
        self.correct_letters_set=set()
        self.present_letters_set=set()
        previous_guesses=set()
        guess_count=0
        if verbose_bool:
            finish_info_function=lambda target_word,guess_count,words_left:print(f"Target word {target_word} found in {guess_count} guesses, {len(words_left)} possible words left")
            iteration_info_function=lambda next_guess,words_left:print(f"Guess: {next_guess}, {len(words_left)} possible words left")
        else:
            finish_info_function=lambda target_word,guess_count,words_left:None
            iteration_info_function=lambda next_guess,words_left:None

        while True:
            strategy_inputs=[
                        self._filter_handler.possible_wordle_words_set,
                        self._filter_handler.potential_letters_dict,
                        self._filter_handler.unique_letters_dict,
                        present_letters_set,
                        self._filter_handler.correct_letters_count_set,
                        invalid_letters_set,
                        all_possible_words,
                        previous_guesses,
                        game_strategy
                    ]
            # strategy_inputs=[
            #             self._filter_handler.possible_wordle_words_set,
            #             self._filter_handler.potential_letters_dict,
            #             self._filter_handler.unique_letters_dict,
            #             self.present_letters_set,
            #             self._filter_handler.correct_letters_count_set,
            #             self.invalid_letters_set,
            #             all_possible_words,
            #             previous_guesses,
            #             game_strategy
            #         ]
            guess_count+=1
            next_guess=implement_strategy(*strategy_inputs)
            if next_guess==target_word:
                finish_info_function(target_word,guess_count,self._filter_handler.possible_wordle_words_set)
                break
            iteration_info_function(next_guess,self._filter_handler.possible_wordle_words_set)
            previous_guesses.add(next_guess) #this will be removed
            #remove guess from possible words, within try as some strategies can suggest invalid words
            try:
                self._filter_handler.possible_wordle_words_set.remove(next_guess)
            except KeyError:
                pass
            t0=perf_counter()
            # incorrect_letters,correct_letters,verified_present_letters=self.evaluate_word(next_guess)
            # present_letters_set=present_letters_set.union(verified_present_letters)
            # invalid_letters_set=invalid_letters_set.union(incorrect_letters)
            verified_present_letters_dict=self.evaluate_word_2(next_guess)
            # separate filtering functions
            # t0=perf_counter()
            # self._filter_handler.handle_present_letters(verified_present_letters)
            # self._filter_handler.handle_correct_letters(correct_letters)
            # self._filter_handler.handle_invalid_letters(incorrect_letters)            
            print(perf_counter()-t0)
            # present_letters_set=present_letters_set.union(verified_present_letters_set)
            # joint filtering functions
            # self._filter_handler.handle_input_letters(incorrect_letters,verified_present_letters,correct_letters)
            self._filter_handler.handle_input_letters(self.invalid_letters_set,self.present_letters_set,verified_present_letters_dict,self.correct_letters_set)
            # self._filter_handler.handle_input_letters(self.invalid_letters_set,self.present_letters_set,correct_letters)
            # print(perf_counter()-t0)
        return guess_count,self._filter_handler.possible_wordle_words_set