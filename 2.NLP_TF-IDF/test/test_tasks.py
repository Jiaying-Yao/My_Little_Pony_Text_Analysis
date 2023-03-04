import unittest
from pathlib import Path
import os, sys
import json
import pandas as pd
from src.compile_word_counts import *
from src.compute_pony_lang import *

parentdir = Path(__file__).parents[1]
sys.path.append(parentdir)


class TasksTest(unittest.TestCase):
    def setUp(self):
        dir = os.path.dirname(__file__)
        self.mock_dialog = os.path.join(dir, 'fixtures', 'mock_dialog.csv')
        self.true_word_counts = os.path.join(dir, 'fixtures', 'word_counts.true.json')
        self.true_tf_idfs = os.path.join(dir, 'fixtures', 'tf_idfs.true.json')
        self.list_pony = ['twilight sparkle', 'fluttershy', 'applejack', 'rarity', 'pinkie pie', 'rainbow dash']
        
        

    def test_task1(self):
        # use  self.mock_dialog and self.true_word_counts; REMOVE self.assertTrue(True) and write your own assertion, i.e. self.assertEquals(...)
        print("\nRUNNING TESTS FOR compile_word_counts.py")
        dialogs = pd.read_csv(self.mock_dialog)[['pony','dialog']]
        dialogs = clean(dialogs)
        my_counts = word_count_allpony(dialogs, False)
        f = open(self.true_word_counts, 'r')
        true_counts = json.load(f)
        f.close()
        self.assertEqual(my_counts, true_counts)
        print('Correct word count for all ponies!')

    def test_task2(self):
        # use self.true_word_counts self.true_tf_idfs; REMOVE self.assertTrue(True) and write your own assertion, i.e. self.assertEquals(...)
        print("\nRUNNING TESTS FOR compute_pony_lang.py")
        f = open(self.true_word_counts, 'r')
        counts_js = json.load(f)
        f.close()
        my_tfidf = js_tfidf(counts_js)
        f2 = open(self.true_tf_idfs, 'r')
        true_tfidf = json.load(f2)
        f2.close()
        self.assertEqual(my_tfidf, true_tfidf)
        print('Correct tf-idf for all ponies!')
        
    
if __name__ == '__main__':
    unittest.main()