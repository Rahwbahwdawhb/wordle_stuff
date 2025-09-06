from functools import partial
import random
try:
    from solver_utils import filter_handler,game_handler
    from solver_strategies import strategy_1
except ModuleNotFoundError:
    1
fh=filter_handler()
gh=game_handler(fh)
# gh.start_noninteractive_game('tower',verbose_bool=True)

correct_letter_conditions=[
lambda correct_letters: len(correct_letters)==0,
lambda correct_letters: len(correct_letters)<=1,
lambda correct_letters: len(correct_letters)<=3,
lambda correct_letters: len(correct_letters)<=4,
lambda correct_letters: len(correct_letters)<=5,
lambda correct_letters: 4<=len(correct_letters),
lambda correct_letters: 3<=len(correct_letters),
lambda correct_letters: 2<=len(correct_letters),
lambda correct_letters: True,
lambda correct_letters: False,
]

def test_strategy_variations(strategy,correct_letter_conditions,target_word_generator,N_iter=10):
    N_conditions=len(correct_letter_conditions)
    all_guess_counts_dict={key:[] for key in [1,2,3,4,5,6,'Fail']}
    last_len=0
    for i,correct_letter_condition in enumerate(correct_letter_conditions):
        guess_counts_dict={key:[] for key in [1,2,3,4,5,6,'Fail']}
        for it in range(N_iter):
            msg=f"Condition {i+1}/{N_conditions}: iteration {it+1}/{N_iter}"
            print(f"\r{msg}{' '*max(0,last_len-len(msg))}",end='',flush=True)
            last_len=len(msg)
            guess_count,words_left=gh.start_noninteractive_game(game_strategy=partial(strategy,correct_letter_condition=correct_letter_condition),target_word=target_word_generator())
            if guess_count<=6:
                guess_counts_dict[guess_count].append(len(words_left))
            else:
                guess_counts_dict['Fail'].append(len(words_left))
        for key,values in guess_counts_dict.items():
            all_guess_counts_dict[key].append(values)
    print(flush=True)
    return all_guess_counts_dict

N_iter=10
target_word_generator=lambda:'tower'
# target_word_generator=lambda:next(iter(fh.wordle_words_dict.keys()))
# target_word_generator=lambda:random.choice(list(fh.wordle_words_dict.keys()))
all_guess_counts_dict=test_strategy_variations(strategy_1,correct_letter_conditions,target_word_generator=target_word_generator,N_iter=N_iter)

print_str=''
for key,values in all_guess_counts_dict.items():
    print_str+=f"Guess {key}:\n"
    for i,condition_values in enumerate(values):
        N=0
        sum_total=0
        for v in condition_values:
            N+=1
            sum_total+=v
        if N>0:
            _mean=sum_total/N
            var=0
            for v in condition_values:
                var+=(v-_mean)**2
            std=var**.5/N**.5
            print_str+=f"Strategy {i}: {100*N/N_iter:1f}%, {_mean:1f}±{std:1f} words left\n"
        else:
            print_str+=f"Strategy {i}: {0}%\n"
# print(print_str)

#0.0002438000519759953, joint filter
#2.600019797682762e-06, union

#1.1699972674250603e-05, union utanför