# My Little Pony Language Analysis
## Task 1: Basic My Little Pony Talking Stats 
In this and the next homework, we’re going to be analyzing My Little Pony language.
Data Source: https://www.kaggle.com/liury123/my-little-pony-transcript
For the purpose of this study, we’ll use only clean_dialog.csv and assume that the dataset is perfect.

### 1. dialog_analysis.py 
Computes and produces a JSON-formatted result that has two keys: count shows the number of speech acts that each character has in the entire file. verbosity gives fraction of dialogue, measured in # of speech acts produced by this pony. For both cases, we only want to see the values related to the six ponies (the main characters of the cartoon).
run: **python3 dialog_analysis.py -o output.json clean_dialog.csv** or **python3 dialog_analysis.py -o output.json clean_dialog_grading.csv**

## Task 2: TF-IDF
### 1. compile_word_counts.py
computes word counts for each pony from all episodes of MLP.
run: **python compile_word_counts.py -o /path/to/word_counts.json -d path/to/clean_dialog.csv**
#### Other details:
1. Valid speech acts - only consider speech acts where the speaker is an exact match for one of the main
character ponies. Ignore any others. Also lines which involve multiple characters, i.e. "Twilight and
Fluttershy" or inexact matches, such as “future Twilight Sparkle” should be ignored.
2. Treat each word encountered as case insensitive. Store words in all lowercase form.
3. Before processing text, replace punctuation characters with a space – a punctuation character is one of
these: ( ) [ ] , - . ? ! : ; # &
4. A word must only include alphabetic characters. All other words should be ignored.
5. Remove the stopwords (listed here -
https://gist.githubusercontent.com/larsyencken/1440509/raw/53273c6c202b35ef00194d06751d8ef630e
53df2/stopwords.txt)

### 2. compute_pony_lang.py
It should compute the **<num_words>** for each pony that has the highest TF-IDF score.
run: **python compute_pony_lang.py -c <pony_counts.json> -n <num_words>**

### 3. Test folder
Unittest

## Task 3: Network Modeling
### 1. build_interaction_network.py
In this part, we are modeling the interaction network as who speaks to who. There is an (undirected)
edge between two characters that speak to one another. The weight of the edge is how many times they
speak to one another.
To keep our life simple, we’re going to use a very simple proxy for “speaking to one another”. We will say that
character X speaks to character Y whenever character Y has a line IMMEDIATELY after character X in an
episode. So, for the following excerpt of dialog from an episode…
Twilight Sparkle: Hey Pinkie. Sorry I accused you of being nosy.
Pinkie Pie: It’s okay, Twilight – we all have our rough days.
Applejack: Come on, everypony! We need to get a move-on.
Spike: Hurray!
In this excerpt, we have the following interactions:
Twilight Sparkles speaks to Pinkie Pie
Pinkie Pie speaks to Apple Jack
Applejack speaks to Spike
Of course, from the text, we can see that Pinkie Pie’s comment wasn’t *really* addressed to Apple Jack…
highlighting how proxies can be wrong. But for this assignment, we’re going to assume it’s a good proxy.
run: **python build_interaction_network.py -i /path/to/<script_input.csv> -o /path/to/<interaction_network.json>**

### 2. compute_network_stats.py
Using the networkx library, compute
- The top three most connected characters by # of edges.
- The top three most connected characters by sum of the weight of edges.
- The top three most central characters by *betweenness*.
run: **python compute_network_stats.py -i /path/to/<interaction_network.json> -o /path/to/<stats.json>**