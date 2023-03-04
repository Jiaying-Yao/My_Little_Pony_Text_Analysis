import pandas as pd
import json
import sys

input_file = sys.argv[2]
output_file = sys.argv[3]
#print(input_file)
df = pd.read_csv(input_file)

ts_count,_ = df[df['pony'].str.lower()=='twilight sparkle'].shape
aj_count,_ = df[df['pony'].str.lower()=='applejack'].shape
rrt_count,_ = df[df['pony'].str.lower()=='rarity'].shape
pp_count,_ = df[df['pony'].str.lower()=='pinkie pie'].shape
rd_count,_ = df[df['pony'].str.lower()=='rainbow dash'].shape
fs_count,_ = df[df['pony'].str.lower()=='fluttershy'].shape
#print(ts_count, aj_count, rrt_count, pp_count, rd_count, fs_count)

total,_ = df.shape
ts_verbo = round (ts_count/total, 2)
aj_verbo = round(aj_count/total, 2)
rrt_verbo = round(rrt_count/total, 2)
pp_verbo = round(pp_count/total, 2) 
rd_verbo = round(rd_count/total, 2)
fs_verbo = round(fs_count/total, 2)

js = {"count":
     {
         "twilight sparkle" : ts_count, "applejack" : aj_count, "rarity" : rrt_count, "pinkie pie" : pp_count, "rainbow dash" : rd_count, "fluttershy" : fs_count
     },
     "verbosity":
      {
          "twilight sparkle" : ts_verbo, "applejack" : aj_verbo, "rarity" : rrt_verbo, "pinkie pie" : pp_verbo, "rainbow dash" : rd_verbo, "fluttershy" : fs_verbo
      }
     }
#print(js)
with open(output_file, 'w') as file:
    json.dump(js, file, indent=4)