import importlib.resources as resources
from os.path import dirname,join,abspath

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
            for word in words.strip().split('\n'):        
                if len(word)!=5:
                    continue
                self.possible_wordle_words_set.add(word)

                #counting occurrences outside of the letter add_word-function
                #to only loop once through the word, and not once for each character
                temp_count_dict=dict()
                temp_position_dict=dict()
                for i,ch in enumerate(word):
                    temp_count_dict[ch]=temp_count_dict.get(ch, 0)+1
                    temp_position_dict.setdefault(ch,{i}).add(i)
                self.unique_letters_dict[word]=len(temp_count_dict)
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
        for i,ch in enumerate(word):
            if (i,ch) in self. target_word_position_set:
                correct_letters.add((i,ch))
                correct_letters_count[ch]=correct_letters_count.get(ch,0)+1
            elif ch in self.target_word_letter_count_dict:
                present_letters.add((i,ch))
            else:
                incorrect_letters.add(ch)
        verified_present_letters=set()
        for i,ch in present_letters:
            if ch in correct_letters_count and correct_letters_count[ch]==self.target_word_letter_count_dict[ch]:
                incorrect_letters.add(ch)
            else:
                verified_present_letters.add((i,ch))
        return incorrect_letters,correct_letters,verified_present_letters
    def start_noninteractive_game(self,game_strategy,target_word=None,verbose_bool=False):
        self._filter_handler.reset()
        all_possible_words=set(self._filter_handler.wordle_words_dict.keys())
        if not target_word:
            target_word=next(iter(self._filter_handler.possible_wordle_words_set))
        self.parse_target_word(target_word)
        invalid_letters_set=set()
        present_letters_set=set()
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
            guess_count+=1
            next_guess=implement_strategy(*strategy_inputs)
            if next_guess==target_word:
                finish_info_function(target_word,guess_count,self._filter_handler.possible_wordle_words_set)
                break
            iteration_info_function(next_guess,self._filter_handler.possible_wordle_words_set)
            previous_guesses.add(next_guess)
            incorrect_letters,correct_letters,verified_present_letters=self.evaluate_word(next_guess)
            present_letters_set=present_letters_set.union(verified_present_letters)
            invalid_letters_set=invalid_letters_set.union(incorrect_letters)
            self._filter_handler.handle_present_letters(verified_present_letters)
            self._filter_handler.handle_correct_letters(correct_letters)
            self._filter_handler.handle_invalid_letters(incorrect_letters)
        return guess_count,self._filter_handler.possible_wordle_words_set