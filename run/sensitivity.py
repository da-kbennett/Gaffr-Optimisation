import pandas as pd
from pathlib import Path
import sys
import argparse

def read_sensitivity(options=None):

    if options is None or options.get('gw') is None:
        gw = int(input("What GW are you assessing? "))
        situation = input("Is this a wildcard? (y/n) ")
    else:
        gw = options['gw']
        situation = options.get('situation', 'n')

    print()

    directory = '../data/results/'
    # no_plans = len(os.listdir(directory))

    if situation == "N" or situation == "n": 

        buys = []
        sells = []
        captains = []
        vice_captains = []
        emergency_captains = []
        starts = []
        squad = []
        no_plans = 0

        for filename in Path(directory).glob("*.csv"):
            plan = pd.read_csv(filename)
            if plan[(plan['week']==gw) & (plan['transfer_in']==1)]['name'].to_list() == []:
                buys += ['No transfer']
                sells += ['No transfer']
            else:
                buy_list = plan[(plan['week']==gw) & (plan['transfer_in']==1)]['name'].to_list()
                buy = ', '.join(buy_list)
                buys.append(buy)

                sell_list = plan[(plan['week']==gw) & (plan['transfer_out']==1)]['name'].to_list()
                sell = ', '.join(sell_list)
                sells.append(sell)
            
            captains += plan[(plan['week']==gw) & (plan['captain']==1) & (plan['transfer_out']!=1)]['name'].to_list()
            vice_captains += plan[(plan['week']==gw) & (plan['vicecap']==1) & (plan['transfer_out']!=1)]['name'].to_list()
            emergency_captains += plan[(plan['week']==gw) & (plan['emergencycaptain']==1) & (plan['transfer_out']!=1)]['name'].to_list()
            starts += plan[(plan['week']==gw) & (plan['lineup']==1) & (plan['transfer_out']!=1)][['name', 'xP']].values.tolist()
            squad += plan[(plan['week']==gw) & (plan['squad']==1) & (plan['transfer_out']!=1)]['name'].to_list()
            no_plans += 1

        # Calculate average xP for each player
        starts_df = pd.DataFrame(starts, columns=['player', 'xP'])
        average_xP = starts_df.groupby('player')['xP'].mean().reset_index()
        average_xP.rename(columns={'xP': 'average_xP'}, inplace=True)

        buy_sum = pd.DataFrame(buys, columns=['player']).value_counts().reset_index(name='PSB')
        sell_sum = pd.DataFrame(sells, columns=['player']).value_counts().reset_index(name='PSB')
        caps = pd.DataFrame(captains, columns=['player']).value_counts().reset_index(name='PSB')
        vices = pd.DataFrame(vice_captains, columns=['player']).value_counts().reset_index(name='PSB')
        emergencies = pd.DataFrame(emergency_captains, columns=['player']).value_counts().reset_index(name='PSB')
        
        # Create squad_counts DataFrame
        squad_counts = pd.DataFrame({'player': squad})
        squad_counts = squad_counts['player'].value_counts().reset_index()
        squad_counts.columns = ['player', 'squad_count']

        # Create starts_counts DataFrame
        starts_counts = pd.DataFrame(starts, columns=['player', 'xP'])  # Make sure 'starts' is a list of tuples [(player_name, xP), ...]
        starts_counts = starts_counts['player'].value_counts().reset_index()
        starts_counts.columns = ['player', 'starts_count']

        
        # Merge average xP with squad_and_lineup DataFrame
        squad_and_lineup = pd.merge(squad_counts, starts_counts, on='player', how='outer').fillna(0)
        squad_and_lineup = pd.merge(squad_and_lineup, average_xP, on='player', how='left')
        # Calculate percentage and sort DataFrame
        squad_and_lineup['percentage'] = (squad_and_lineup['starts_count'] / squad_and_lineup['squad_count']) * 100
        squad_and_lineup = squad_and_lineup.sort_values(by='percentage', ascending=False)
        squad_and_lineup['percentage'] = squad_and_lineup['percentage'].astype(int).astype(str) + '%'

        squad_and_lineup_avxp = squad_and_lineup.sort_values(by='average_xP', ascending=False)
        
        buy_sum['PSB'] = ["{:.0%}".format(buy_sum['PSB'][x]/no_plans) for x in range(buy_sum.shape[0])]
        sell_sum['PSB'] = ["{:.0%}".format(sell_sum['PSB'][x]/no_plans) for x in range(sell_sum.shape[0])]
        
        caps['PSB'] = ["{:.0%}".format(caps['PSB'][x]/no_plans) for x in range(caps.shape[0])]
        vices['PSB'] = ["{:.0%}".format(vices['PSB'][x]/no_plans) for x in range(vices.shape[0])]
        emergencies['PSB'] = ["{:.0%}".format(emergencies['PSB'][x]/no_plans) for x in range(emergencies.shape[0])]

        # Assuming you have already defined squad_and_lineup, buy_sum, sell_sum, caps, vices, and emergencies dataframes

        
        print('Buy:')
        print('\n'.join(buy_sum.to_string(index = False).split('\n')[1:]))
        print()
        print('Sell:')
        print('\n'.join(sell_sum.to_string(index = False).split('\n')[1:]))
        print()
        print('Who to stick the armband on:')
        print('\n'.join(squad_and_lineup_avxp[['player', 'average_xP']].to_string(index=False, float_format="%.2f").split('\n')[1:]))
        print()
        print('Makes the starting lineup:')
        print('\n'.join(squad_and_lineup[['player', 'percentage']].to_string(index=False, float_format="%.2f").split('\n')[1:]))
    
    elif situation == "Y" or situation == "y":

        goalkeepers = []
        defenders = []
        midfielders = []
        forwards = []
        captains = []
        vice_captains = []
        emergency_captains = []
        starts = []
        squad = []

        no_plans = 0

        for filename in Path(directory).glob("*.csv"):
            plan = pd.read_csv(filename)
            goalkeepers += plan[(plan['week']==gw) & (plan['pos']=='GKP') & (plan['transfer_out']!=1)]['name'].to_list()
            defenders += plan[(plan['week']==gw) & (plan['pos']=='DEF') & (plan['transfer_out']!=1)]['name'].to_list()
            midfielders += plan[(plan['week']==gw) & (plan['pos']=='MID') & (plan['transfer_out']!=1)]['name'].to_list()
            forwards += plan[(plan['week']==gw) & (plan['pos']=='FWD') & (plan['transfer_out']!=1)]['name'].to_list()
            captains += plan[(plan['week']==gw) & (plan['captain']==1) & (plan['transfer_out']!=1)]['name'].to_list()
            vice_captains += plan[(plan['week']==gw) & (plan['vicecap']==1) & (plan['transfer_out']!=1)]['name'].to_list()
            emergency_captains += plan[(plan['week']==gw) & (plan['emergencycaptain']==1) & (plan['transfer_out']!=1)]['name'].to_list()
            starts += plan[(plan['week']==gw) & (plan['lineup']==1) & (plan['transfer_out']!=1)]['name'].to_list()
            squad += plan[(plan['week']==gw) & (plan['squad']==1) & (plan['transfer_out']!=1)]['name'].to_list()
            no_plans += 1

        keepers = pd.DataFrame(goalkeepers, columns=['player']).value_counts().reset_index(name='PSB')
        defs = pd.DataFrame(defenders, columns=['player']).value_counts().reset_index(name='PSB')
        mids = pd.DataFrame(midfielders, columns=['player']).value_counts().reset_index(name='PSB')
        fwds = pd.DataFrame(forwards, columns=['player']).value_counts().reset_index(name='PSB')
        caps = pd.DataFrame(captains, columns=['player']).value_counts().reset_index(name='PSB')
        vices = pd.DataFrame(vice_captains, columns=['player']).value_counts().reset_index(name='PSB')
        emergencies = pd.DataFrame(emergency_captains, columns=['player']).value_counts().reset_index(name='PSB')
        squad_counts = pd.Series(squad).value_counts().reset_index()
        squad_counts.columns = ['player', 'squad_count']
        starts_counts = pd.Series(starts).value_counts().reset_index()
        starts_counts.columns = ['player', 'starts_count']
        squad_and_lineup = pd.merge(squad_counts, starts_counts, on='player', how='outer').fillna(0)        
        squad_and_lineup['percentage'] = (squad_and_lineup['starts_count'] / squad_and_lineup['squad_count']) * 100
        squad_and_lineup = squad_and_lineup.sort_values(by='percentage', ascending=False)
        squad_and_lineup['percentage'] = squad_and_lineup['percentage'].astype(int).astype(str) + '%'

        keepers['PSB'] = ["{:.0%}".format(keepers['PSB'][x]/no_plans) for x in range(keepers.shape[0])]
        defs['PSB'] = ["{:.0%}".format(defs['PSB'][x]/no_plans) for x in range(defs.shape[0])]
        mids['PSB'] = ["{:.0%}".format(mids['PSB'][x]/no_plans) for x in range(mids.shape[0])]
        fwds['PSB'] = ["{:.0%}".format(fwds['PSB'][x]/no_plans) for x in range(fwds.shape[0])]
        caps['PSB'] = ["{:.0%}".format(caps['PSB'][x]/no_plans) for x in range(caps.shape[0])]
        vices['PSB'] = ["{:.0%}".format(vices['PSB'][x]/no_plans) for x in range(vices.shape[0])]
        emergencies['PSB'] = ["{:.0%}".format(emergencies['PSB'][x]/no_plans) for x in range(emergencies.shape[0])]

        print('Goalkeepers:')
        print('\n'.join(keepers.to_string(index = False).split('\n')[1:]))
        print()
        print('Defenders:')
        print('\n'.join(defs.to_string(index = False).split('\n')[1:]))
        print()
        print('Midfielders:')
        print('\n'.join(mids.to_string(index = False).split('\n')[1:]))
        print()
        print('Forwards:')
        print('\n'.join(fwds.to_string(index = False).split('\n')[1:]))
        print()
        print('Captains:')
        print('\n'.join(caps.to_string(index = False).split('\n')[1:]))
        print()
        print('Vice Captains:')
        print('\n'.join(vices.to_string(index = False).split('\n')[1:]))
        print()
        print('Emergency Captains:')
        print('\n'.join(emergencies.to_string(index = False).split('\n')[1:]))
        print()
        print('Makes the starting lineup:')
        print('\n'.join(squad_and_lineup[['player', 'percentage']].to_string(index=False).split('\n')[1:]))

        return {'keepers': keepers, 'defs': defs, 'mids': mids, 'fwds': fwds, 'caps': caps, 'vices': vices, 'emergencies': emergencies, 'squad_and_lineup': squad_and_lineup}

    else:
        print("Invalid input, please enter 'y' for a wildcard or 'n' for a regular transfer plan.")

if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(description='Summarize sensitivity analysis results')
        parser.add_argument("--gw", type=int, help="Numeric value for 'gw'")
        parser.add_argument("--wildcard", choices=['Y', 'y', 'N', 'n'], help="'Y' if using wildcard, 'N' otherwise")
        args = parser.parse_args()
        gw_value = args.gw
        is_wildcard = args.wildcard
        read_sensitivity({'gw': gw_value, 'situation': is_wildcard})
    except:
        read_sensitivity()