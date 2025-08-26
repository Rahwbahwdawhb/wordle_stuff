possible_words_lister
    Package to list possible Wordle words given remaining/spare letters
    The reference words are taken from words_alpha.txt, which was obtained
    from: https://github.com/dwyl/english-words?tab=readme-ov-file

Installation:
pip install git+https://github.com/Rahwbahwdawhb/wordle_stuff

Android installation:
1.  Download Termux from the Play store
2.  Open Termux and run:
     2.1 pkg install python3
     2.2 pkg install git
3a. Global installation:
    3a.1 pip install git+https://github.com/Rahwbahwdawhb/wordle_stuff
    3a.2 To uninstall: pip uninstall 
3b. Virtual environment installation:
    3b.1 python3 -m venv myvenv
    3b.2 source myvenv/bin/activate
    3b.3 pip install git+https://github.com/Rahwbahwdawhb/wordle_stuff

Run script:
1a. If globally installed:
    1a.1 check
1b. If installed in a Virtual environment:
    1b.1 If not active: source myvenv/bin/activate 
    1b.2 check
    1b.3 To deactivate: deactivate