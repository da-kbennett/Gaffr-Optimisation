import os
import sys
import pathlib
import json
import pandas as pd
import argparse
import random
import string
import datetime


def get_random_id(n):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(n))

def solve_regular(runtime_options=None):

    base_folder = pathlib.Path()
    sys.path.append(str(base_folder / "../src"))
    from multi_period_dev import prep_data, solve_multi_period_fpl
    import data_parser as pr
    
    regular_settings_filename = f"regular_settings.json"        
    with open(f'../data/{regular_settings_filename}') as f:
        options = json.load(f)

    parser = argparse.ArgumentParser(add_help=False)
    for key in options.keys():
        if isinstance(options[key], (list, dict)):
            continue

        parser.add_argument(f"--{key}", default=options[key], type=type(options[key]))

    args = parser.parse_known_args()[0]
    options = {**options, **vars(args)}

    if runtime_options is not None:
        options = {**options, **runtime_options}

    if options.get("cbc_path") != "" and options.get("cbc_path") is not None:
        os.environ['PATH'] += os.pathsep + options.get("cbc_path")

    if options.get("preseason"):
        my_data = {'picks': [], 'chips': [], 'transfers': {'limit': None, 'cost': 4, 'bank': 1000, 'value': 0}}    
    else:
        try:                
            regular_team_json = f"team.json"            
            with open(f'../data/{regular_team_json}') as f:
                my_data = json.load(f)
        except FileNotFoundError:
            print(
                """You must either:
                    1. Download your team data and save it under data folder with name 'team.json', or
                    2. Set "team_data" in regular_settings to "ID", and set the "team_id" value to your team's ID
                """)
            exit(0)
    data = prep_data(my_data, options)

    response = solve_multi_period_fpl(data, options)
    run_id = get_random_id(5)    

    for result in response:
        iter = result['iter']
        print(result['summary'])
        time_now = datetime.datetime.now()
        stamp = time_now.strftime("%Y-%m-%d_%H-%M-%S")
        if not (os.path.exists("../data/results/")):
            os.mkdir("../data/results/")
        result['picks'].to_csv(f"../data/results/regular_{stamp}_{run_id}_{iter}.csv")
    
    result_table = pd.DataFrame(response)
    print(result_table[['iter', 'sell', 'buy', 'score']])

    # Detailed print
    for result in response:
        picks = result['picks']
        gws = picks['week'].unique()
        print(f"Solution {result['iter']+1}")
        for gw in gws:
            line_text = ''
            chip_text = picks[picks['week']==gw].iloc[0]['chip']
            if chip_text != '':
                line_text += '(' + chip_text + ') '
            sell_text = ', '.join(picks[(picks['week'] == gw) & (picks['transfer_out'] == 1)]['name'].to_list())
            buy_text = ', '.join(picks[(picks['week'] == gw) & (picks['transfer_in'] == 1)]['name'].to_list())
            if sell_text != '':
                line_text += sell_text + ' -> ' + buy_text
            else:
                line_text += "Roll"
            print(f"\tGW{gw}: {line_text}")


if __name__=="__main__":
    solve_regular()