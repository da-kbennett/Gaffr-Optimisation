from unicodedata import combining, normalize
import pandas as pd
import requests
from fuzzywuzzy import fuzz
import numpy as np


def read_data(options, source):
    if source == 'gaffr':
        data = pd.read_csv(options.get('data_path', '../data/gaffr.csv'))
        data['gaffr_id'] = data['ID']
        return data
    


# To remove accents in names
def fix_name_dialect(name):
    new_name = ''.join([c for c in normalize('NFKD', name) if not combining(c)])
    return new_name.replace('Ø', 'O').replace('ø', 'o').replace('ã', 'a')

def get_best_score(r):
    return max(r['wn_score'], r['cn_score'])



