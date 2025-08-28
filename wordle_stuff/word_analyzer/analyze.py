import importlib.resources as resources
from os.path import dirname,join,abspath
from sys import argv

def add_to_count_dict(_dict,key):
    if key in _dict:
        _dict[key]+=1
    else:
        _dict[key]=1
def count_dict(_dict):
    max_key_count=(0,'')
    total_key_counts=0
    key_counts=len(_dict)
    for key,count in _dict.items():
        total_key_counts+=count
        if max_key_count[0]<count:
            max_key_count=(count,key)
    return max_key_count,key_counts,total_key_counts
class count_holder:
    """
    Utilities class that holds counts of most common (max) key, number of keys and
    total key counts from nodes' parents_dict, bases_dict and children_dict
    """
    def __init__(self,parents_dict,children_dict,bases_dict):
        self.max_parent_count,self.unique_parents_count,self.total_parents_count=count_dict(parents_dict)
        self.max_base_count,self.unique_bases_count,self.total_bases_count=count_dict(bases_dict)
        self.max_child_count,self.unique_children_count,self.total_children_count=count_dict(children_dict)
class node:
    """
    Node for word tree structure, has the following attributes:
    character = a letter in the word that is being split into nodes
    bases_dict = a dictionary with all possible prepending letter 
                 combinations as keys and the number of times they
                 occur as values
    parents_dict = a dictionary with all possible prepending letters as keys
                   and the number of times they occur as values
    children_dict = a dictionary with all possible subsequent letters as keys
                    and the number of times they occur as values
    """
    def __init__(self,character,base,parent):
        self.character=character
        self.bases_dict=dict()
        self.parents_dict=dict()
        self.add_base_parent(base,parent)
        self.children_dict=dict()
    def add_child(self,child):
        if child.character in self.children_dict:
            self.children_dict[child.character]+=1
        else:
            self.children_dict[child.character]=1
    def add_base_parent(self,base,parent):
        if isinstance(parent,node):
            parent.add_child(self)
            parent_character=parent.character
        else:
            parent_character=''
        add_to_count_dict(self.parents_dict,parent_character)
        add_to_count_dict(self.bases_dict,base)
    def get_count_holder(self):
        return count_holder(self.parents_dict,self.children_dict,self.bases_dict)

def get_nodes(word_file="wordle_words.txt"):
    """
    Read a file that contains a list of words (one word per row) and create a five
    layer (one for each possible letter position) tree structure, with each letter
    that appear in the given letter position making up a node. Each word thus 
    correspond to a distinct path through the tree structure.

    Input:
    word_file = the name of the word file
    Outputs:
    all_nodes_dict = dictionary with (letter_index,letter) as keys and node objects as values
    valid_word_count = total number of 5 letter words from which all_nodes_dict is generated
    """
    all_nodes_dict=dict()
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
        valid_word_count=0
        for word in words.strip().split('\n'):        
            if len(word)!=5:
                continue
            valid_word_count+=1
            last_node=None
            temp_set=set()
            for i,ch in enumerate(word):
                temp_set.add(ch)
                if (i,ch) in all_nodes_dict:
                    node_i=all_nodes_dict[(i,ch)]
                    node_i.add_base_parent(word[:i],last_node)
                else:
                    node_i=node(ch,word[:i],last_node)
                    all_nodes_dict[(i,ch)]=node_i
                last_node=node_i
    return all_nodes_dict,valid_word_count
def inspect_nodes(all_nodes_dict,valid_word_count):
    """
    Loop through node dictionary generated from get_nodes, 
    and print information about every letter position.

    Inputs:
    all_nodes_dict = dictionary with (letter_index,letter) as keys and node objects as values
    valid_word_count = total number of 5 letter words from which all_nodes_dict is generated
    """
    most_common_character_dict={i:(0,None,None) for i in range(5)}
    for (layer,ch),_node in all_nodes_dict.items():
        _count_holder=_node.get_count_holder()
        most_common_count_reference=max(_count_holder.total_children_count,_count_holder.total_parents_count)
        if most_common_character_dict[layer][0]<most_common_count_reference:
            most_common_character_dict[layer]=(most_common_count_reference,ch,_count_holder)

    for layer in range(5):
        analysis_str=f"Letter-position {layer+1}:\n"
        analysis_str+=f"Is most commonly {most_common_character_dict[layer][1]} ({most_common_character_dict[layer][0]} times), which:\n"
        analysis_str+=f" -occurs in {100*most_common_character_dict[layer][0]/valid_word_count:.2f}% of the words\n"
        if layer>0:
            analysis_str+=f" -can follow {most_common_character_dict[layer][2].unique_parents_count} unique directly preceeding letters\n"
            analysis_str+=f" -can follow {most_common_character_dict[layer][2].unique_bases_count} unique preceeding letter combinations\n"
            unique_preceeding_count=most_common_character_dict[layer][2].max_base_count[0]
            if unique_preceeding_count>1:
                analysis_str+=f" --the most common of which is {most_common_character_dict[layer][2].max_base_count[1]} ({unique_preceeding_count} times)\n"
            else:
                analysis_str+=f" --None of which appear more than once\n"
        if layer<4:
            analysis_str+=f" -can lead to {most_common_character_dict[layer][2].unique_children_count} unique directly succeeding letters\n"
        print(analysis_str)
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
        all_nodes_dict,valid_word_count=get_nodes(word_file=word_file)
        inspect_nodes(all_nodes_dict,valid_word_count)

if __name__=='__main__':
    main()