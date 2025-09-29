import pandas as pd
from nltk.corpus import wordnet as wn

from helpers import load_model


nlp_model = load_model()


def get_synonyms_with_similarity(word, pos, nlp_model):
    """
    Gets synonyms of the input word, calculates their similarities and returns a Dataframe sorted by similarity.
    :param word: input word
    :param pos: part of speech of the input word
    :param nlp_model: spacy model used for embeddings
    :return: DataFrame of synonyms and their similarities to the input word
    """
    word_nlp = nlp_model(word)
    if pos is None:
        synsets = wn.synsets(word)
    else:
        pos = [wn.NOUN, wn.VERB, wn.ADJ, wn.ADV][['noun', 'verb', 'adj', 'adv'].index(pos)]
        synsets = wn.synsets(word, pos=pos)
    lemmas = list()
    lemma_names = set()
    for synset in synsets:
        lemmas.extend(synset.lemmas())
    for lemma in lemmas:
        lemma_names.add(str(lemma.name()))
    lemma_names = list(lemma_names)
    if word in lemma_names:
        lemma_names.remove(word)
    elif word.upper() in lemma_names:
        lemma_names.remove(word.upper())

    similarities = [word_nlp.similarity(nlp_model(ln)) for ln in lemma_names]
    syn_sim_df = pd.DataFrame({'synonym': lemma_names, 'similarity': similarities})
    syn_sim_df = syn_sim_df.sort_values('similarity', ascending=False)

    return syn_sim_df


def run_simple_mode(word, pos, max_syn, display_similarities):
    """
    Runs simple mode.
    :param word: input word
    :param pos: part of speech of the input word (for filtering synonyms)
    :param max_syn: maximum number of synonyms to display
    :param display_similarities: display the similarities of the synonyms to the input word
    """
    while not word:
        word = input('Please enter a word:\n>')
        if word == '':
            print('Invalid input!')
    syn_sim_df = get_synonyms_with_similarity(word, pos, nlp_model)
    synonyms = list(syn_sim_df['synonym'])
    similarities = list(syn_sim_df['similarity'])
    output_message = f'Found {len(synonyms)} synonyms of {word + (f' as {pos}' if pos is not None else '')} in wordnet'
    if max_syn is not None and max_syn < len(synonyms):
        output_message += f', displaying first {max_syn} results by similarity'
    print(output_message + (':' if len(synonyms) > 0 else '.'))

    if not display_similarities:
        print(', '.join(synonyms) if (max_syn is not None and len(synonyms) <= max_syn) else ', '.join(synonyms[:max_syn]))
    else:
        syn_sim = [synonyms[i] + f' ({round(similarities[i], 2)})' for i in range(len(synonyms))]
        print(', '.join(syn_sim) if (max_syn is not None and len(syn_sim) <= max_syn) else ', '.join(syn_sim[:max_syn]))
