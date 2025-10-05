
#point assigners
def get_letter_in_words_assigner(letter_in_words_dict):
    return (lambda ch,i,count: letter_in_words_dict[ch],'inner') #words should be removed from this dict when they are removed from possible_words, need inverting dict
def get_vowel_point_assigner():
    vowels={'a','e','i','o','u','y'}
    return (lambda ch,i,count: 5+count-1 if ch in vowels else 0,'outer') #unique vowels score higher
def get_position_point_assigner(position_words_dict):
    return (lambda ch,i,count: len(position_words_dict[(i,ch)]),'inner')
def get_unique_letter_assigner(unique_letters_dict):
    return (lambda word:unique_letters_dict[word],'word')

def assign_points(word,point_assigners,overall_word_letter_dict,points,cache_dict):
    worse_guess_bool=False
    exceed_bool=False
    temp_point_dict={i:0 for i,_ in enumerate(point_assigners)}
    for iter_ch,ch_countPositions in enumerate(overall_word_letter_dict[word].items()):
        ch,(count,positions)=ch_countPositions
        for (iter_la,point),la in zip(points.items(),point_assigners):
            if la[1]=='word':
                if iter_ch==0:
                    point_iter=la[0](word)
                    if point_iter<point:
                        worse_guess_bool=True
                        break
                    if point_iter>point:
                        exceed_bool=True
                    temp_point_dict[iter_la]=point_iter
                else:
                    continue
            else:
                if la[1]=='inner':
                    point_iter=0
                    for i,_ in positions:
                        if (la[0],ch,i,count) not in cache_dict:
                            cache_dict[(la[0],ch,i,count)]=la[0](ch,i,count)
                        point_iter+=cache_dict[(la[0],ch,i,count)]
                        # point_iter+=la[0](ch,i,count)
                else:
                    i=0
                    if (la[0],ch,i,count) not in cache_dict:
                        cache_dict[(la[0],ch,i,count)]=la[0](ch,i,count)
                    point_iter=cache_dict[(la[0],ch,i,count)]
                    # point_iter=la[0](ch,0,count)
                temp_point_dict[iter_la]+=point_iter
                if iter_ch==4:
                    if temp_point_dict[iter_la]<point: #reached end of word and point is lower than current max point
                        worse_guess_bool=True
                        break
                    if temp_point_dict[iter_la]>point:
                        exceed_bool=True
        if worse_guess_bool and not exceed_bool:
            break
    return exceed_bool,temp_point_dict
