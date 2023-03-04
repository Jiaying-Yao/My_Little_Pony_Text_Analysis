'''
1.
Build an undirected network between characters, not only ponies
by their conversaitons
run python3 build_interaction_network.py -i <input csv> -o <output json>
ran python3 build_interaction_network.py -i ../../../hw3/submission_template/data/pony_data/clean_dialog.csv -o ../interaction_network.json
'''
import networkx as nx
import pandas as pd
import numpy as np
import argparse
import os
import os.path as osp
import json

def check_word(name, forbidden):
    if set(str.split(name, " ")) & set(forbidden):
        return True
    else:
        return False

def build_network(df, forbidden, top_101):
    G = nx.Graph()
    pony_prev = df['pony'][0]
    title_prev = df['title'][0]

    for i in range(1,len(df)):
        title = df['title'][i]
        pony = df['pony'][i]

        #pony cannot speak to itself
        if pony == pony_prev:
            pony_prev = pony
            title_prev = title
            
        #character name has to follow the rules
        if set(forbidden) & set(str.split(pony, " ")) or pony not in top_101:
            pony_prev = None
            title_prev = title
            continue

        #change in episode stops the network
        if title != title_prev:
            #print('New episode started')
            pony_prev = pony
            title_prev = title
            continue

        #add weight
        if pony_prev != None:
            if G.has_edge(pony_prev, pony):
                G[pony_prev][pony]['weight'] = G[pony_prev][pony]['weight'] + 1
            else:
                G.add_edge(pony_prev, pony, weight=1)
    
        pony_prev = pony
        title_prev = title
    return G

def main():
    #read commendline argument
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input')
    parser.add_argument('-o', '--output')
    args = parser.parse_args()
    input = args.input
    output = args.output

    df = pd.read_csv(input)
    #clean df, choose only 101 ponies
    df = df.loc[:,['title', 'pony']].apply(lambda x: x.astype(str).str.lower())
    forbidden = ['others', 'ponies', 'and', 'all']
    counts = df['pony'].value_counts()
    df_count = pd.DataFrame()
    df_count['name']= counts.index
    df_count['counts'] = list(counts)
    df_count = df_count[df_count['name'].apply(lambda x: not check_word(x, forbidden))]
    top_101 = list(df_count[0:101]['name'])


    G = build_network(df, forbidden, top_101)

    #pos=nx.spring_layout(G)
    #nx.draw(G,pos)
    labels = nx.get_edge_attributes(G, 'weight')
    #nx.draw_networkx_edge_labels(G, pos,edge_labels=labels)
    #extract weights from label
    js = {}
    for speaker1 in top_101:
        js[speaker1] = {}
        for speaker2 in top_101:
            if speaker1 == speaker2: continue
            try:
                js[speaker1][speaker2] = labels[(speaker1, speaker2)]
            except KeyError as err:
                try:
                    js[speaker1][speaker2] = labels[(speaker2, speaker1)]
                except KeyError as err:
                    continue

    #export json
    os.makedirs(osp.dirname(output), exist_ok=True)
    with open(output, 'w') as f:
        f.truncate(0)
        json.dump(js, f, indent = 4)
    f.close()
    
    

if __name__ == '__main__':
    main()