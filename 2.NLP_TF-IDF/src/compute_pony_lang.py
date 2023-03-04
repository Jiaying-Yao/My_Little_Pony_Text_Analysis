'''
2. 
run python3 compute_pony_lang.py -c pony_counts.json -n <num>
ran python3 compute_pony_lang.py -c ../word_counts.json -n 5
return json with ponies and their <num> words with highest tf-idf
tf(word, pony) = num of times this pony said this word
idf(word, script) = log10(total num of ponies / num of ponies said the word)
'''
import pandas as pd
import json
import math
import argparse
import os.path as osp

list_pony = ['twilight sparkle', 'fluttershy', 'applejack', 'rarity', 'pinkie pie', 'rainbow dash']
#input a df with rows of words and columns of num of time a pony said the word, and num of ponies said the word
def tfidf(word, num_pony_total, script):
    tf = script.loc[word, 'count']
    num_said_word = script.loc[word, 'num_pony']
    idf = math.log10(num_pony_total/num_said_word)
    tfidf_num = '%.9f'%(tf*idf)
    return float(tfidf_num)

#from a packed json, extract a dataframe for a pony: (pony_name:rows of words it said), count: a column with count, a column with count of ponies said the word
def extract_count(js, pony):
    df = pd.DataFrame.from_dict(js)
    df.loc[:,'num_pony'] = df.count(axis=1)
    pony_df = df.loc[:,[pony,'num_pony']].dropna()
    pony_df.loc[:,'count'] = pony_df[pony]
    pony_df = pony_df.drop(columns=[pony])
    return pony_df

#return json with all ponies and words with tfidf scores
def js_tfidf(js):
    tfidf_ponies = dict()
    for pony in list_pony:
        pony_df = extract_count(js, pony)
        pony_df.loc[:,'words'] = pony_df.index
        pony_df.loc[:,pony] = pony_df['words'].apply(lambda x: tfidf(x, 6, pony_df))
        pony_df = pony_df.sort_values(by=pony, ascending=False)
        #pony_df.index = pony_df['words']
        pony_df = pony_df.drop(columns=['words', 'num_pony','count'])
        tfidf_pony = pony_df.to_dict()
        tfidf_ponies = {**tfidf_ponies, **tfidf_pony}
        
    return tfidf_ponies



def main():
    #read commendline arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--counts')
    parser.add_argument('-n', '--number')
    args = parser.parse_args()
    pony_counts = args.counts
    num = int(args.number)

    #read pony_counts.json into counts_df
    pony_counts = open(pony_counts, 'r')
    counts_js = json.load(pony_counts)
    tfidf_ponies = js_tfidf(counts_js)
    with open('../try2.json', 'w') as f:
        json.dump(tfidf_ponies, f, indent=4)
    output_js = dict()
    
    for key in tfidf_ponies:
        words = tfidf_ponies[key]
        words_list = [word for word in words][0:num]
        
        output_js[key] = words_list
    
    print(json.dumps(output_js,indent=4)) 



if __name__ == '__main__':
    main()
