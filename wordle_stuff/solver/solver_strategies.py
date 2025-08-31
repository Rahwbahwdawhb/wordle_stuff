import random

def filter_guesses(start_set,sum_function):
        guesses=[]
        _count=0
        for _v in start_set:
            _sum=sum_function(_v)
            if _count<_sum:
                guesses=[_v]
                _count=_sum
            elif _count==_sum:
                guesses.append(_v)
        return guesses,_count

def implement_strategy(possible_wordle_words_set,potential_letters_dict,
                       unique_letters_dict,present_letters_set,correct_letters_set,
                       invald_letters_set,all_words_set,previous_guesses,
                       strategy_function,mandatory_filter_functions=[]):
    N_possible=len(possible_wordle_words_set)
    if N_possible==1:
        next_guess=next(iter(possible_wordle_words_set))
    else:
        guess_list=strategy_function(possible_wordle_words_set,potential_letters_dict,
                       unique_letters_dict,present_letters_set,correct_letters_set,
                       invald_letters_set,all_words_set,previous_guesses)
        if not guess_list:
            guess_list=list(possible_wordle_words_set)
        for filter_function in mandatory_filter_functions:
            guess_list,_=filter_guesses(guess_list,filter_function)
        next_guess=random.choice(guess_list)
    return next_guess

def strategy_1(possible_wordle_words_set,potential_letters_dict,
                       unique_letters_dict,present_letters_set,correct_letters_set,
                       invald_letters_set,all_words_set,previous_guesses):
    present_letters_set_2={ch for _,ch in present_letters_set}
    correct_indices=set()
    correct_letters=set()
    for i,ch in correct_letters_set:
        correct_indices.add(i)
        correct_letters.add(ch)
    guess_list=[]
    # if len(correct_letters)==0:
    # if len(correct_letters)<=1:
    if len(correct_letters)<=2:
    # if len(correct_letters)<=3:
    # if len(correct_letters)<=4:
    # if len(correct_letters)<=5:
    # if 4<=len(correct_letters):
    # if 3<=len(correct_letters):
    # if 2<=len(correct_letters):
    # if True:
    # if False:
        non_correct_letters=set()
        for word in possible_wordle_words_set:
            for ch in word:
                if ch not in correct_letters:
                    non_correct_letters.add(ch)
        non_correct_count=0
        for word in all_words_set:
            temp_set=set()
            ok=True
            invalid_sum=0
            for i,ch in enumerate(word):
                if ch in invald_letters_set\
                or (i,ch) in present_letters_set\
                or (i,ch) in correct_letters_set\
                    or (ch in present_letters_set_2 and i in correct_indices):
                    ok=False
                    break
                elif ch in non_correct_letters:
                    temp_set.add(ch)
                elif ch in invald_letters_set:
                    invalid_sum+=1
            if not ok:
                continue
            temp_count=len(temp_set)-invalid_sum
            if non_correct_count<temp_count:
                guess_list=[word]
                non_correct_count=temp_count
            elif non_correct_count==temp_count:
                guess_list.append(word)
    return guess_list