from setuptools import setup, find_packages
setup(     
     name="wordle_stuff",     
     version="1.0",
     python_requires=">=3.10",   
     packages=find_packages(),
     package_data={
        'wordle_stuff': ['data_files/words_alpha.txt','data_files/wordle_words.txt']
    },
    entry_points={
        'console_scripts': [
            'check = wordle_stuff.possible_words_lister.check:main',
            'analyze = wordle_stuff.word_analyzer.analyze:main',
        ],
    }
)