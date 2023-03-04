import pandas as pd
word_list = ['apple', 'apple', 'b', 'c']
df = pd.DataFrame(word_list).value_counts().rename_axis(word_list[1]).reset_index(name=word_list[2])
print(df)