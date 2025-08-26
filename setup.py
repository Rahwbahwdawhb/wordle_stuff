from setuptools import setup, find_packages
setup(     
     name="possible_words_lister",     
     version="0.1",
     python_requires=">=3.10",   
     packages=find_packages(),
     package_data={
        'possible_words_lister': ['words_alpha.txt']
    },
    entry_points={
        'console_scripts': [
            'check = possible_words_lister.check:main',
        ],
    }
)