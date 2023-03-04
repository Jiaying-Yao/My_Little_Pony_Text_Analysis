'''
2.
run python3 compute_network_stats.py -i <input.json> -o <output_stat.json>
ran python3 compute_network_stats.py -i ../interaction_network.json -o ../stats.json
find out top3 ponies with the most friends
top3 ponies with the most concersation to others
top3 ponies the most important
'''
import json
import argparse
import networkx as nx
import pandas
import os
import os.path as osp

def main():
    #read commendline arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input')
    parser.add_argument('-o', '--output')
    args = parser.parse_args()
    input = args.input
    output = args.output

    f = open(input, 'r')
    js = json.load(f)
    f.close()

    #top3 most connected
    js_connection = {}
    for speaker in js:
        js_connection[speaker]=len(js[speaker].items())
    sorted_l = list(js_connection.items())
    sorted_l.sort(key=lambda x: -x[1])
    top3_edges = [t[0] for t in sorted_l][0:3]
    
    #top3 sum of weights
    js_weights = {}
    for speaker in js:
        js_weights[speaker]=sum(map(lambda x: x[1], js[speaker].items()))

    sorted_w = list(js_weights.items())
    sorted_w.sort(key=lambda x: -x[1])
    top3_weights = [t[0] for t in sorted_w][0:3]

    #top3 centrality betweenness
    G = nx.Graph()
    for speaker1 in js:
        for speaker2 in js[speaker1]:
            weight = js[speaker1][speaker2]
            G.add_edge(speaker1, speaker2, weight = weight)

    bc = nx.betweenness_centrality(G)
    sorted_bc = list(bc.items())
    sorted_bc.sort(key=lambda x: -x[1])
    top3_bc = [t[0] for t in sorted_bc][0:3]

    stat = {}
    stat["most_connected_by_num"] = top3_edges
    stat["most_connected_by_weight"] = top3_weights
    stat["most_central_by_betweenness"] = top3_bc

    os.makedirs(osp.dirname(output), exist_ok=True)
    with open(output, 'w') as f:
        f.truncate(0)
        json.dump(stat, f, indent = 4)
    f.close()

if __name__ == '__main__':
    main()