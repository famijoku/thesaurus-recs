from pywsd import simple_lesk
from nltk.corpus import wordnet as wn

from helpers import sort_synonyms_by_similarity, load_model
nlp_model = load_model()

def run_interactive_mode(word, pos, max_syn, display_similarities): # ADD POS FUNCTIONALITY
    while not word:
        word = input('Please enter a word:\n>')
        if word == '':
            print('Invalid input!')
    context = input('Enter the context of the word (optional)\n>')
    slesk_result = simple_lesk(context, word)
    print(f'WSD result: {slesk_result} ({slesk_result.definition()})')
    action = input('[c]ontinue with this sense, [l]ist all senses or [q]uit?\n>')
    while action != 'q':
        if action not in 'cl':
            print('Invalid Input!')
            print(f'WSD result: {slesk_result} ({slesk_result.definition()})')
            action = input('[c]ontinue with this sense, [l]ist all senses or [q]uit?\n>')
        elif action == 'c':
            chosen_sense = slesk_result
            break
        elif action == 'l':
            for id, sense in enumerate(wn.synsets(word)):
                print(f'{id}: {sense} ({sense.definition()})')
            choice = input('\nEnter the number of the sense of choice or [c]ancel:\n>')
            if choice == 'c':
                print(f'WSD result: {slesk_result} ({slesk_result.definition()})')
                action = input('[c]ontinue with this sense, [l]ist all senses or [q]uit?\n>')
            else:
                try:
                    chosen_sense = wn.synsets(word)[int(choice)]
                    break
                except IndexError:
                    print('Invalid index! Pick one of the listed senses or [c]ancel.\n')
                except ValueError:
                    print('Invalid input! Enter one of the listed integer indices or [c]ancel.\n')
    if action == 'q':
        print('Quitting')
    else:
        print(f'Continuing with sense {chosen_sense}')
        syn_sim_df = sort_synonyms_by_similarity(word, chosen_sense, nlp_model)
        synonyms = list(syn_sim_df['synonym'])
        similarities = list(syn_sim_df['similarity'])
        print(f'Found {len(synonyms)} synonyms for chosen sense in wordnet' +
              (f', displaying {max_syn} most similar' if max_syn is not None and max_syn < len(synonyms) else '')
              + (':' if len(synonyms) > 0 else '.'))
        for i in range(len(synonyms) if (max_syn is None or len(synonyms) < max_syn) else max_syn):
            print(synonyms[i] + (f' ({str(round(similarities[i], 2))})' if display_similarities else ''))
