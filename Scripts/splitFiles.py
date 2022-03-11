import csv
import pandas as pd

matchdf = pd.read_csv('data/raw/matches.csv')
lanedf = pd.read_csv('data/raw/lanediff.csv')
championdf = pd.read_csv('data/raw/champions.csv')

filteredMatchdf = pd.read_csv('data/filtered/filteredMatch.csv')
filteredLanedf = pd.read_csv('data/filtered/filteredLane.csv')
traindf = pd.read_csv('data/filtered/trainMatch.csv')

def getFilterMatch():
    ids = timelinedf['match id'].unique()

    filtermatch = matchdf[matchdf['match id'].isin(ids)]

    filtermatch.to_csv('filteredMatch.csv', index=False)

def splitMatchData():
    shuffeddf = filtereddf.sample(frac=1)

    shuffeddf.head(1500).to_csv('testMatch.csv', index=False)
    shuffeddf.iloc[1500:3000].to_csv('validationMatch.csv', index=False)
    shuffeddf.iloc[3000:].to_csv('trainMatch.csv', index=False)

def getFilterLane():
    ids = traindf['match id'].unique()

    filterlane = lanedf[lanedf['match id'].isin(ids)]

    filterlane.to_csv('filteredLane.csv', index=False)

def getPositionWinRate():
    champions = championdf['id']

    winRatedf = pd.DataFrame(columns=['position', 'champion id', 'win rate'])

    for i in champions:
        for position in range(5):
            df1 = traindf[traindf.iloc[:, position] == i]
            df2 = traindf[traindf.iloc[:, position+5] == i]

            count = len(df1) + len(df2)

            win = len(df1[df1['match result'] == 'blue']) + len(df2[df2['match result'] == 'red'])

            winRate = 0.5
            if count > 0:
                winRate = round(win / count, 3)

            dic = {
                'position': position,
                'champion id': i,
                'win rate': winRate
            }

            winRatedf = winRatedf.append(dic, ignore_index=True)

    winRatedf.to_csv('positionalChampionWinRate.csv', index=False)

def getSynergy():
    champions = championdf['id']

    synergydf = pd.DataFrame(columns=['champion 1', 'champion 2', 'win rate'])

    idx = 0
    for i in champions:
        idx += 1
        for j in champions[idx:]:
            df1 = (traindf.iloc[:, :5] == i).any(axis=1)
            df2 = (traindf.iloc[:, :5] == j).any(axis=1)
            df3 = (traindf.iloc[:, 5:10] == i).any(axis=1)
            df4 = (traindf.iloc[:, 5:10] == j).any(axis=1)

            blue = traindf[df1 & df2]
            red = traindf[df3 & df4]

            count = len(blue) + len(red)
            win = len(blue[blue['match result'] == 'blue']) + len(red[red['match result'] == 'red'])

            dic1 = {
                'champion 1': i,
                'champion 2': j,
                'win rate': 0.5
            }
            dic2 = {
                'champion 1': j,
                'champion 2': i,
                'win rate': 0.5
            }

            if count > 0:
                dic1['win rate'] = round(win / count, 3)
                dic2['win rate'] = round(win / count, 3)
                
            synergydf = synergydf.append(dic1, ignore_index=True)
            synergydf = synergydf.append(dic2, ignore_index=True)

    synergydf.to_csv('synergy.csv', index=False)
    
getSynergy()

def getLaneAvg():
    champions = championdf['id']

    laneDiffAvgdf = pd.DataFrame(columns=['position', 'player 1', 'player 2', 'gold diff', 'xp diff', 'win rate'])

    dic = {
        'position': None,
        'player 1': None,
        'player 2': None,
        'gold diff': 0,
        'xp diff': 0,
        'win rate': 0.5
    }

    idx = 0
    for i in champions:
        idx += 1
        for j in champions[idx:]:
            if i != j:
                for position in range(5):
                    lanedf1 = filteredLanedf[(filteredLanedf['player 1'] == i)
                                        & (filteredLanedf['player 2'] == j)
                                        & (filteredLanedf['position'] == position)]
                    lanedf2 = filteredLanedf[(filteredLanedf['player 1'] == j)
                                        & (filteredLanedf['player 2'] == i)
                                        & (filteredLanedf['position'] == position)]

                    count = len(lanedf1) + len(lanedf2)

                    if count == 0:
                        dic['position'] = position
                        dic['player 1'] = i
                        dic['player 2'] = j
                        laneDiffAvgdf = laneDiffAvgdf.append(dic, ignore_index=True)

                        dic['player 1'] = j
                        dic['player 2'] = i
                        laneDiffAvgdf = laneDiffAvgdf.append(dic, ignore_index=True)
                    else:
                        a = lanedf1.sum()
                        b = lanedf2.sum()

                        match1 = traindf[(traindf.iloc[:, position] == i)
                                         & (traindf.iloc[:, position+5] == j)
                                         & (traindf.iloc[:, 10] == 'blue')]
                        match2 = traindf[(traindf.iloc[:, position] == j)
                                         & (traindf.iloc[:, position+5] == i)
                                         & (traindf.iloc[:, 10] == 'red')]

                        dic1 = {
                            'position': position,
                            'player 1': i,
                            'player 2': j,
                            'gold diff': int((a['gold diff'] - b['gold diff']) / count),
                            'xp diff': int((a['xp diff'] - b['xp diff']) / count),
                            'win rate': round((len(match1) + len(match2)) / count, 3)
                        }

                        dic2 = {
                            'position': position,
                            'player 1': j,
                            'player 2': i,
                            'gold diff': -int((a['gold diff'] - b['gold diff']) / count),
                            'xp diff': -int((a['xp diff'] - b['xp diff']) / count),
                            'win rate': round(1 - round((len(match1) + len(match2)) / count, 3), 3)
                        }

                        laneDiffAvgdf = laneDiffAvgdf.append(dic1, ignore_index=True)
                        laneDiffAvgdf = laneDiffAvgdf.append(dic2, ignore_index=True)

    laneDiffAvgdf.to_csv('laneAvg.csv', index=False)
