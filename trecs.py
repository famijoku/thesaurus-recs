import nltk
import warnings
import argparse

from config import config


def main():
    if config['suppress_warnings']:
        warnings.filterwarnings("ignore", message='.*vectors.*')

    try:
        nltk.data.find('corpora/wordnet')
    except LookupError:
        nltk.download('wordnet')

    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', '-m',
                        action='store',
                        choices=['simple', 'interactive', 'document'],
                        default='simple',
                        help='Simple: suggests synonyms ranked by similarity,'
                             'Interactive: uses word sense disambiguation based on given context,'
                             'Document: takes an input file, if no word is given')
    parser.add_argument('--word', '-w',
                        action='store',
                        help='Word for which synonyms are to be displayed (optional in document mode)',
                        default=None)
    parser.add_argument('--pos',
                        action='store',
                        choices=['noun', 'verb', 'adj', 'adv'],
                        help='Enter part of speech to facilitate synonym finding')
    parser.add_argument('--exclude', '-x',
                        action='store',
                        nargs='+',
                        help='exclude words from being counted for the most frequent words in document mode (can take multiple arguments)',
                        default=[])
    parser.add_argument('--max',
                        action='store',
                        type=int,
                        default=config['default_max_synonyms'],
                        help='Maximum number of synonyms to display per word')
    parser.add_argument('--file', '-f',
                        action='store',
                        help='Path to file for document mode')
    parser.add_argument('--display_similarities',
                        action='store_true',
                        default=config['default_display_similarities'],
                        help='Display similarities of found synonyms based on word embeddings from SpaCy')
    parser.add_argument('--number_of_words', '-n',
                        action='store',
                        type=int,
                        default=config['default_number_of_words'],
                        help='For document mode without specified word: number of most frequent words for which to display synonyms')
    parser.add_argument('--full_context',
                        action='store_true',
                        help='For document mode: use whole text as context (assume only one word sense)')
    args = parser.parse_args()


    if args.mode == 'simple':
        from simple_mode import run_simple_mode

        run_simple_mode(word=args.word,
                        pos=args.pos,
                        max_syn=args.max,
                        display_similarities=args.display_similarities)
    elif args.mode == 'interactive':
        from interactive_mode import run_interactive_mode

        run_interactive_mode(word=args.word,
                             pos=args.pos,
                             max_syn=args.max,
                             display_similarities=args.display_similarities)
    else:
        from document_mode import run_document_mode

        run_document_mode(input_file=args.file,
                          word=args.word,
                          pos=args.pos,
                          excluded=args.exclude,
                          number_of_words=args.number_of_words,
                          max_syn=args.max,
                          display_similarities=args.display_similarities,
                          full_context=args.full_context)


if __name__ == '__main__':
    main()
