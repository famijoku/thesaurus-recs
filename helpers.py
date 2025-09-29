import spacy
from spacy.util import is_package
import pandas as pd
import subprocess
import sys

from config import config


def load_model():
    if config['model'] == 'large':
        model = 'en_core_web_lg'
    else:
        model = 'en_core_web_sm'

    if not is_package(model):
        subprocess.check_call([sys.executable, '-m', 'spacy', 'download', model])
    return spacy.load(model)


def sort_synonyms_by_similarity(word, synset, nlp_model):
    word_nlp = nlp_model(word)
    lemma_names = [str(lemma.name()) for lemma in synset.lemmas()]
    if word in lemma_names:
        lemma_names.remove(word)
    elif word.upper() in lemma_names:
        lemma_names.remove(word.upper())

    similarities = [word_nlp.similarity(nlp_model(ln)) for ln in lemma_names]
    syn_sim_df = pd.DataFrame({'synonym': lemma_names, 'similarity': similarities})
    syn_sim_df = syn_sim_df.sort_values('similarity', ascending=False)

    return syn_sim_df