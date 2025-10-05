import solver_utils as su
from time import time
from point_assigners import assign_points,get_letter_in_words_assigner,get_unique_letter_assigner,get_position_point_assigner,get_vowel_point_assigner
fh=su.filter_handler()
#point assigners

letter_in_words_assigner=get_letter_in_words_assigner(fh.letter_in_words_dict)
unique_letter_assigner=get_unique_letter_assigner(fh.unique_letters_dict)
position_point_assigner=get_position_point_assigner(fh.position_words_dict)
vowel_point_assigner=get_vowel_point_assigner()

# words=['tower','tooth','flake']
words=fh.possible_wordle_words_set

point_assigners_list=[unique_letter_assigner,position_point_assigner,letter_in_words_assigner,vowel_point_assigner]

from itertools import permutations
def get_permutation_dict(a):
    return {n: list(permutations(a, n)) for n in range(1, len(a)+1)}

point_assigners_permutation_dict=get_permutation_dict(point_assigners_list)
# for _key,_list in point_assigners_permutation_dict.items():
#     for _perm in _list:
#         print(f"{_key}: {_perm}")


# point_assigners=[vowel_point_assigner,unique_letter_assigner,position_point_assigner,letter_in_words_assigner]

for N_point_assigners,point_assigners_permutations in point_assigners_permutation_dict.items():
    for pi,point_assigners in enumerate(point_assigners_permutations):
        points={i:0 for i,_ in enumerate(point_assigners)}
        cache_dict=dict()
        guess=''
        t0=time()
        for word in words:
            exceed_bool,temp_point_dict=assign_points(word,point_assigners,fh.overall_word_letter_dict,points,cache_dict)
            if exceed_bool:
                points=temp_point_dict
                guess=word
        print((N_point_assigners,pi),time()-t0,points,guess)