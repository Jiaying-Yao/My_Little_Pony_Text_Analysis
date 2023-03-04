'''
1. 
run python3 compile_word_counts.py -o <word_counts.json(output)> -d <dialog.csv>
ran python3 compile_word_counts.py -o ../word_counts.json -d ../../../hw3/submission_template/data/pony_data/clean_dialog.csv
organize dialogs of pony, output to word_counts.json
use "clean_dialog.py" in hw3
'''
import os
import os.path as osp
import argparse
from typing import Dict
import pandas as pd
import json
import re

list_pony = ['twilight sparkle', 'fluttershy', 'applejack', 'rarity', 'pinkie pie', 'rainbow dash']

def clean(df):
    #read stop words file
    dir = osp.dirname(__file__)
    stop_path = osp.join(dir, '..', 'data', 'stopwords.txt')
    stops = pd.read_csv(stop_path, sep = '\n')
    stops = stops['#'].values.tolist()[5:]

    #special characters
    chars = "[\(\)\[\]\,\-\.\?\!\:\;\#\&\]]"

    # keep only valid dialogs: exact match with pony names
    # replace special characters by space then convert each dialog into list of words
    #make sure each word only contains alphabetical characters

    df.loc[:,'dialog'] = df['dialog'].str.lower()
    df.loc[:,:] = df[df.pony.str.lower().isin(list_pony)]
    df.loc[:,'dialog'] = df['dialog'].apply(lambda x: re.sub(chars, ' ', str(x)))
    df.loc[:,'dialog'] = df['dialog'].apply(lambda x: [word for word in str(x).split(' ') if (word not in stops and word != '' and word.isalpha() == True)])

    return df

def word_count(df, col_name1, col_name2, word_limit = False):
    #return df with words and counts in word_list
    #word_limit: we only count for these words
    word_list = sum(df['dialog'], [])
    if word_limit is not False:
        word_list = [word for word in word_list if word in word_limit]
    df = pd.DataFrame(word_list).value_counts().rename_axis(col_name1).reset_index(name=col_name2)
    return df

def word_count_allpony(dialogs, word_limit):
    output_json = dict()
    for pony in list_pony:
        pony_df = dialogs[dialogs['pony'].str.lower() == pony]
        pony_count = word_count(pony_df, 'word', pony, word_limit=word_limit)
        pony_count.index = pony_count['word']
        pony_count=pony_count.drop(columns=['word'])
        
        pony_json = pony_count.to_dict()

        output_json = {**output_json, **pony_json}
    return output_json

def main():

    #read commendline arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output')
    parser.add_argument('-d', '--dialog')

    args = parser.parse_args()
    output_file = args.output
    dialog_file = args.dialog

    #read dialog file and clean: return col1 = pony col2 = dialog(list of words)
    dialogs = pd.read_csv(dialog_file)[['pony','dialog']]
    dialogs = clean(dialogs)

    #all_words = sum(dialogs['dialog'],[])
    total_word_count = word_count(dialogs, 'word', 'count')

    #remove words with count<5
    #now we only count these words
    print("Counting for all words...(might takes a while)")
    total_word_count = total_word_count[total_word_count['count']>=5]
    word_limit=list(total_word_count['word'])
    
    #output json
    output_json = word_count_allpony(dialogs, word_limit)

    os.makedirs(osp.dirname(output_file), exist_ok = True)
    with open(output_file, 'w') as out:
        out.truncate(0)
        json.dump(output_json, out, indent = 4)
    out.close()


if __name__ == "__main__":
    main()