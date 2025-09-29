config = {
    'model': 'small',                       # set to 'large' to use spacy model en_core_web_lg, 'small' to use en_core_web_sm
    'default_display_similarities': False,  # default choice for displaying synonym similarities
    'default_number_of_words': 3,           # [document mode] default value for number of most frequent words, for which synonyms are retrieved
    'default_max_synonyms': None,           # default value for truncating output after that many synonyms, set to None for no limit
    'excluded_words': [],                   # exclude words from being counted for the most frequent words in document mode
    'docmode_context_window': 8,            # how many tokens before and after the word are to be used as context in document mode
    'suppress_warnings': True               # suppress warnings from spacy (relevant when evaluating similarity of words without embedding)
}