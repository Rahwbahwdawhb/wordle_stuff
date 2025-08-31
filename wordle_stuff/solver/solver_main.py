try:
    from solver_utils import filter_handler,game_handler
    from solver_strategies import strategy_1
except ModuleNotFoundError:
    1
fh=filter_handler()
gh=game_handler(fh)
# gh.start_noninteractive_game('tower',verbose_bool=True)

target_word='tower'
N_iter=10
guess_counts_dict={key:[] for key in [1,2,3,4,5,6,'Fail']}
from time import time
t0=time()
for it in range(N_iter):
    print(f"{it}/{N_iter}",end='\r',flush=True)
    guess_count,words_left=gh.start_noninteractive_game(game_strategy=strategy_1)
    # guess_count,words_left=gh.start_noninteractive_game(target_word)
    # guess_count,words_left=gh.start_noninteractive_game(target_word,verbose_bool=True)
    if guess_count<=6:
        guess_counts_dict[guess_count].append(len(words_left))
    else:
        guess_counts_dict['Fail'].append(len(words_left))
for key,values in guess_counts_dict.items():
    print(f"{key}: {100*len(values)/N_iter}")
duration=time()-t0
print(duration/N_iter,duration)