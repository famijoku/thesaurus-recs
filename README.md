## Thank you for installing, and welcome to Thesaurus Recs., a synonym suggestor based on WordNet in NLTK and SpaCy.

This program generally searches for synonyms in WordNet and ranks the results by similarity to the input word, using word embeddings from SpaCy[^1]. The exact function depends on the mode used. Modes are specified using --mode (-m). The modes are simple, interactive and document.


### Setup:

If not already installed, you will first need to install python (Thesaurus Recs uses Python 3.13).
Then, in the terminal, navigate to your thesaurus_recs folder, create and activate your virtual environment, install the required packages and execute the setup.py:

On Linux or MacOS:
```
$ python -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```
On Windows:
```
thesaurus-recs> python -m venv venv
thesaurus-recs> venv\Scripts\activate
thesaurus-recs> pip install -r requirements.txt
```

On further use, you will only need to activate the venv again (2nd line) and you'll be able to use Thesaurus Recs with:

```
$ python3 trecs.py [options]
```
```
thesaurus-recs> python trecs.py [options]
```
on Windows.

### The options:

`--mode` (`-m`)
The mode in which to run Thesaurus Recs. Valid arguments are `simple`, `interactive` and `document`. If not specified, simple mode is used.

`--word` (`-w`)
The word for which synonyms will be retrieved. Required in simple and interactive mode, optional in document mode.

`--pos`
Part of speech of the specified word (relevant for simple mode, interactive mode and document mode if `--full_context` is used). Helps facilitate word sense disambiguation. Valid options are `noun`, `verb`, `adj`, and `adv`.

`--file` (`-f`)
Path to the input file for document mode.

`--max`
Maximum number of synonyms to display. Default can be set in the config.py. *Note: this may not always be beneficial, as synonyms that do not have an embedding in SpaCy will be assigned a similarity of 0 and will therefore be relatively low in the ranking.*

`--display_similarities`
Display the calculated similarities of the synonyms to the input word. This can be turned on by default in the config.py.

`--full_context`
For document mode with a word specified: use the entire text as context, one word sense will be assumed for all occurrences.

`--number_of_words` (`-n`)
For document mode without a word specified: simple mode will be performed on the n most frequent non-stopwords. Default is 3, but can be changed in the config.py.

`--exclude` (`-x`)
For document mode without a word specified: words to ignore when looking for the most frequent words. Can take several arguments. Words to be excluded by default can be added in the config.py.


### The config.py:
In this file, you can change some of the default behaviours. You can set or change:
- `model`: which model to use (valid values: `'large'` for en_core_web_lg, `'small'` for en_core_web_sm)
- `default_max_synonyms`: the default maximum number of synonyms to display (any positive integer, or `None` for no limit)
- `default_display_similarities`: whether or not to display the similarities by default (`True` or `False`)
- `default_number_of_words`: the default number of most frequent words for which to seach for synonyms in document mode (any positive integer)
- `excluded_words`: a list of words to be excluded by default from being counted for the most frequent words in document mode (list of strings)
- `docmode_context_window`: how many non-stopword tokens before and after each occurrence of the input word are to be used as context for WSD in document mode (any positive integer)
- `suppress_warnings`: whether or not to suppress warnings from SpaCy about 
    - distance calculations with empty vectors (if a synonym has no vector representation)
    - using the small model, which does not use word vectors


### Simple Mode:
In simple mode, all lemmas of all synonyms of the specified word are retrieved from WordNet, their embeddings (if existent) retrieved from SpaCy, and finally output ranked by similarity[^1].

Options for this mode are:

`--word` (`-w`) [`WORD`]
In simple mode, a word needs to be entered. If not filled, you will be asked to enter a word later.

`--pos` {`noun`, `verb`, `adj`, `adv`}
Part of speech of the input word. In simple mode, this simply filters the output to only include synonyms of the same POS.

`--max` [`MAX`]
Maximum number of synonyms to display. Valid options are: any positive integer. A default value can be set in the config.py.

`--display_similarities`
Display the calculated similarities of the synonyms to the input word. This can be turned on by default in the config.py.

Example usage:
```
$ python3 trecs.py -w cold
Found 12 synonyms of cold in wordnet:
cold-blooded, frigid, coldness, stale, dusty, moth-eaten, inhuman, frigidity, insensate, common_cold, low_temperature, frigidness
```
Now, if you decide that you only want the adjectives, that four synonyms are enough, and that you want to know the calculated similarities:
```
$ python3 trecs.py -w cold --pos adj --max 4 --display_similarities
Found 7 synonyms of cold as adj in wordnet, displaying first 4 results by similarity:
cold-blooded (0.76), frigid (0.64), stale (0.41), dusty (0.37)
```
The results of simple mode are mixed from different word senses, and should therefore not be used without considering if the sense is correct - otherwise, your cold drink might just become stale.


### Interactive Mode:
In interactive mode, after entering a word, you can also enter a bit of context. *This is optional, you can leave the context blank.* After that, Word sense disambiguation will be attempted, using pywsd's `simple_lesk()`. This is not perfect, and will in many cases yield a wrong result - therefore you are asked to confirm the chosen sense or pick another one. Finally, the lemmas of the chosen synset are output, sorted by similarity[^1].

Options for this mode are:
`--word` (`-w`) [`WORD`]
In interactive mode, a word needs to be entered. If not filled, you will be asked to enter a word later.

`--pos` {`noun`, `verb`, `adj`, `adv`}
Part of speech of the input word. In interactive mode, this helps with the word sense disambiguation.

`--max` [`MAX`]
Maximum number of synonyms to display. Valid options are: any positive integer. A default value can be set in the config.py.

`--display_similarities`
Display the calculated similarities of the synonyms to the input word. This can be turned on by default in the config.py.

Example usage:

1. 
```
$ python3 trecs.py -m interactive
Please enter a word:
>map
Enter the context of the word (optional)
>map the input values to the output values
WSD result: Synset('map.v.06') (to establish a mapping (of mathematical elements or sets))
[c]ontinue with this sense, [l]ist all senses or [q]uit?
>c
Continuing with sense Synset('map.v.06')
Found 1 synonyms for chosen sense in wordnet:
represent
```

2. 
```
$ python3 trecs.py -m interactive -w fire --pos verb --display_similarities
Enter the context of the word (optional)
>the boss fired an employee
WSD result: Synset('displace.v.03') (terminate the employment of; discharge from an office or position)
[c]ontinue with this sense, [l]ist all senses or [q]uit?
>c
Continuing with sense Synset('displace.v.03')
Found 10 synonyms for chosen sense in wordnet:
can (0.35)
sack (0.23)
dismiss (0.17)
displace (0.15)
terminate (0.13)
give_notice (0.0)
send_away (0.0)
give_the_axe (0.0)
force_out (0.0)
give_the_sack (0.0)
```
Here, we can see that a lot of synonyms have a similarity of 0. This is not because they are dissimilar, but because they have no embedding in the SpaCy model.

3. 
```
$ python3 trecs.py -m interactive -w dagger
Enter the context of the word (optional)
>the killer used a dagger
WSD result: Synset('dagger.n.02') (a character used in printing to indicate a cross reference or footnote)
[c]ontinue with this sense, [l]ist all senses or [q]uit?
>l
0: Synset('dagger.n.01') (a short knife with a pointed blade used for piercing or stabbing)
1: Synset('dagger.n.02') (a character used in printing to indicate a cross reference or footnote)

Enter the number of the sense of choice or [c]ancel:
>0
Continuing with sense Synset('dagger.n.01')
Found 1 synonyms for chosen sense in wordnet:
sticker
```
If you are dissatisfied with the result of the WSD - which may happen quite often - you can pick another word sense, for which synonyms will be listed.


### Document mode:
In document mode, you can either: 
- not enter a word: the most frequent non-stopword and non-excluded words of the document text will be determined, and simple mode will be performed on each of them
- enter a word: if `--full_context` is used, WSD will be performed using the whole document as context and the synonyms for the found sense will be output sorted by similarity. Otherwise, WSD will be performed on each occurrence of the word, using a window of tokens (the size of which can be set in the config.py) around it as context and the synonyms for each sense will be output sorted by similarity. If a certain sense has already appeared, following occurrences assigned that sense will be ignored, as not to output a lot of duplicates for large texts.

Options for this mode are:
`--file` (`-f`) [`FILE`]
Path to the file containing the text. If not filled, you will be asked to enter a path later.

`--word` (`-w`) [`WORD`]
In document mode, a word does not need to be entered. If not filled, simple mode will be performed on the most frequent words.

`--pos` {`noun`, `verb`, `adj`, `adv`}
Part of speech of the input word. In document mode, this helps with the word sense disambiguation, but is only used if a word is entered and `--full_context` is *not* used.

`--max` [`MAX`]
Maximum number of synonyms to display. Valid options are: any positive integer. A default value can be set in the config.py.

`--number_or_words` (`-n`) [NUMBER_OF_WORDS]
If no word is entered, simple mode will be performed on the n most frequent non-stopword and non-excluded words. Valid arguments are any positive integer. Default is 3, but can be changed in the config.py.

`--exclude` (`-x`) [WORD] +
Exclude words from being counted for the most frequent words. Can take several arguments. Words that should *always* be excluded can be set in the config.py.

`--display_similarities`
Display the calculated similarities of the synonyms to the input word (or one of the most frequent words). This can be turned on by default in the config.py.

`--full_context`
If this option is used, a single word sense of the input word will be assumed for all occurrences, and WSD is performed using the entire text as context.

Example usage:

1. No word entered
```
$ python3 trecs.py -m document -f ./testing/macbeth.txt --max 5 --display_similarities
Running document mode. No word specified, searching for synonyms for the 3 most frequent word(s).

Most frequent word: macbeth (285 occurrences)
Found 1 synonyms of macbeth in wordnet:
Macbeth (1.0)


2nd most frequent word: lady (95 occurrences)
Found 7 synonyms of lady in wordnet, displaying first 5 results by similarity:
Lady (1.0), madam (0.51), dame (0.51), ma'am (0.37), gentlewoman (0.32)


3rd most frequent word: thou (90 occurrences)
Found 9 synonyms of thou in wordnet, displaying first 5 results by similarity:
thousand (0.35), K (0.19), M (0.18), G (0.16), yard (0.12)`
```
Here we can see that *Macbeth* has an entry in Wordnet, but of course no relevant synonyms. Furthermore, *thou* is interpreted as a short form of *thousand*. We might want to exclude those two:

```
$ python3 trecs.py -m document -f ./testing/macbeth.txt --max 5 --display_similarities -x macbeth thou
Running document mode. No word specified, searching for synonyms for the 3 most frequent word(s).

Most frequent word: lady (95 occurrences)
Found 7 synonyms of lady in wordnet, displaying first 5 results by similarity:
Lady (1.0), madam (0.51), dame (0.51), ma'am (0.37), gentlewoman (0.32)


2nd most frequent word: enter (65 occurrences)
Found 19 synonyms of enter in wordnet, displaying first 5 results by similarity:
participate (0.55), enroll (0.46), embark (0.38), enrol (0.34), introduce (0.33)


3rd most frequent word: yet (57 occurrences)
Found 18 synonyms of yet in wordnet, displaying first 5 results by similarity:
even (0.75), still (0.74), however (0.72), nonetheless (0.66), nevertheless (0.64)
```
Now we additionally get synonyms for *enter* and *yet*, which are more helpful.

2. Word entered, varying context
```
$ python3 trecs.py -m document -f ./testing/macbeth.txt -w witch --max 5 --display_similarities
Running document mode for word 'witch'.

Found 52 occurrences of witch.

For context "desert place thunder lightning enter three witches first witch three meet thunder lightning rain second witch done" found word sense Synset('witch.n.02') (a being (usually female) imagined to have special powers derived from the devil)
No synonyms found.

For context "women yet beards forbid interpret macbeth speak first witch hail macbeth hail thane second witch hail macbeth" found word sense Synset('hag.n.01') (an ugly evil-looking old woman)
Synonyms for that sense (displaying 5 most similar):
hag (0.54)
crone (0.49)
beldam (0.0)
beldame (0.0)

For context "double toil trouble fire burn cauldron bubble second witch cool baboon blood charm firm good enter hecate" found word sense Synset('hex.v.01') (cast a spell over someone or something; put a hex on someone or something)
Synonyms for that sense:
jinx (0.24)
glamour (0.2)
hex (0.2)
enchant (0.19)
bewitch (0.19)
```
Here, we can see that even though the word *witch* occurs 52 times, only three sets of synonyms are output. This is because all subsequent occurrences have yielded an already seen WSD result. It also becomes apparent that WSD does not always work flawlessly, as the second witch has, in an ironic twist of fate, been turned into a verb.

3. Word entered, full context
```
$ python3 trecs.py -m document -f ./testing/macbeth.txt -w witch --max 5 --display_similarities --full_context
Running document mode for word 'witch', using the whole document as context.

For the given text as context found word sense Synset('hex.v.01') (cast a spell over someone or something; put a hex on someone or something)
Synonyms for that sense:
jinx (0.24)
glamour (0.2)
hex (0.2)
enchant (0.19)
bewitch (0.19)
```
Once again, WSD performs poorly. Here however, we can specify the part of speech as a noun:
```
$ python3 trecs.py -m document -f ./testing/macbeth.txt -w witch --max 5 --display_similarities --full_context --pos noun
Running document mode for word witch, using the whole document as context.

For the given text as context found word sense Synset('witch.n.02') (a being (usually female) imagined to have special powers derived from the devil)
No synonyms found.
```
Here, the correct interpretation is chosen, but sadly WordNet does not have any synonyms for that sense.


[^1]: A similarity of 0 does not necessarily mean a low similarity, most often the word just does not have an embedding in SpaCy.
