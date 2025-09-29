import re
from pywsd import simple_lesk
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
from nltk.tokenize import word_tokenize

from helpers import sort_synonyms_by_similarity, load_model
from simple_mode import run_simple_mode
from config import config


nlp_model = load_model()


def run_document_mode(input_file, word, pos, excluded, number_of_words, max_syn, display_similarities, full_context):
    """
    Runs document mode.
    :param input_file: file from which to read the text
    :param word: word for which to find synonyms (optional in document mode, if not given, n most frequent words will be used)
    :param pos: part of speech of the input word, only relevant if --full_context is used, helps facilitate word sense disambiguation
    :param excluded: list of words to exclude from being counted for the most frequent words
    :param number_of_words: (default n=3) if no word is entered, for n most frequent words, synonyms will be given
    :param max_syn: maximum number of synonyms to output for each word
    :param display_similarities: display similarities of found synonyms (if word is not given)
    :param full_context: use the full document as context, assume only one sense for all occurrences of word
    """
    while not input_file:
        input_file = input('Please enter the path to the input file:\n>')
        if input_file == '':
            print('Invalid input!')
    with open(input_file, 'r', encoding='utf-8') as in_file:
        text = in_file.read()
    stop_words = set(stopwords.words('english'))
    tokens = word_tokenize(text.lower(), language='english')
    filtered_tokens = [word for word in tokens if word not in stop_words and re.match(r'\w+', word) and wn.synsets(word) != []]

    if word is None:
        print(f'Running document mode. No word specified, searching for synonyms for the {number_of_words} most frequent word(s).\n')
        unique_words = set(filtered_tokens)
        excluded.extend(config['excluded_words'])
        for excluded_word in excluded:
            if excluded_word in unique_words:
                unique_words.remove(excluded_word)

        if number_of_words >= len(unique_words):
            number_of_words = len(unique_words)
        for i in range(number_of_words):
            ith_most_frequent = max(unique_words, key=filtered_tokens.count)
            match i:
                case 0:
                    print(f'Most frequent word: {ith_most_frequent} ({filtered_tokens.count(ith_most_frequent)} occurrences)')
                case 1:
                    print(f'2nd most frequent word: {ith_most_frequent} ({filtered_tokens.count(ith_most_frequent)} occurrences)')
                case 2:
                    print(f'3rd most frequent word: {ith_most_frequent} ({filtered_tokens.count(ith_most_frequent)} occurrences)')
                case _:
                    print(f'{i+1}th most frequent word: {ith_most_frequent} ({filtered_tokens.count(ith_most_frequent)} occurrences)')
            run_simple_mode(ith_most_frequent, pos=None, max_syn=max_syn, display_similarities=display_similarities)
            print('\n')
            unique_words.remove(ith_most_frequent)

    elif not full_context:
        print(f"Running document mode for word '{word}'.\n")
        n_occurrences = filtered_tokens.count(word.lower())
        occurrences_with_context = list()
        print(f'Found {n_occurrences} occurrences of {word}.')
        for i in range(n_occurrences):
            occ_index = filtered_tokens.index(word.lower())
            window_before, window_after = (config['docmode_context_window'], config['docmode_context_window'])
            if window_before > occ_index: # shortens window if context before too short
                window_before = occ_index
            if window_after > len(filtered_tokens) - occ_index - 1: # shortens window if context afterwards too short
                window_after = len(filtered_tokens) - occ_index - 1
            occurrences_with_context.append(' '.join(filtered_tokens[(occ_index - window_before):(occ_index + window_after + 1)]))
            filtered_tokens = filtered_tokens[occ_index + 1:]

        seen_synsets = list()
        for occ in occurrences_with_context:
            slesk_result = simple_lesk(occ, word)
            if slesk_result not in seen_synsets: # checks if synset has already been seen, as not to output a lot of duplicates for long texts
                print(f'\nFor context "{occ}" found word sense {slesk_result} ({slesk_result.definition()})')
                syn_sim_df = sort_synonyms_by_similarity(word, slesk_result, nlp_model)
                synonyms = list(syn_sim_df['synonym'])
                similarities = list(syn_sim_df['similarity'])
                print('Synonyms for that sense' +
                      (f' (displaying {max_syn} most similar)' if max_syn is not None and max_syn >
                        len(synonyms) else '') + ':'
                      if len(synonyms) > 0 else 'No synonyms found.')
                for i in range(len(synonyms) if (max_syn is None or len(synonyms) < max_syn) else max_syn):
                    print(synonyms[i] + (f' ({str(round(similarities[i], 2))})' if display_similarities else ''))
                seen_synsets.append(slesk_result)

    else: # no word given, --full_context used
        if pos is not None:
            pos = [wn.NOUN, wn.VERB, wn.ADJ, wn.ADV][['noun', 'verb', 'adj', 'adv'].index(pos)]
        print(f"Running document mode for word '{word}', using the whole document as context.\n")
        slesk_result = simple_lesk(text, word, pos)
        print(f'For the given text as context found word sense {slesk_result} ({slesk_result.definition()})')
        syn_sim_df = sort_synonyms_by_similarity(word, slesk_result, nlp_model)
        synonyms = list(syn_sim_df['synonym'])
        similarities = list(syn_sim_df['similarity'])
        print('Synonyms for that sense' +
              (f' (displaying {max_syn} most similar)' if max_syn is not None and max_syn > len(
                  synonyms) else '') + ':'
              if len(synonyms) > 0 else 'No synonyms found.')
        for i in range(len(synonyms) if (max_syn is None or len(synonyms) < max_syn) else max_syn):
            print(synonyms[i] + (f' ({str(round(similarities[i], 2))})' if display_similarities else ''))
