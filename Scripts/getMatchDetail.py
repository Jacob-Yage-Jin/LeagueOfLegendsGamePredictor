import requests
import csv
import time
import pandas as pd

api_key = 'api_key=RGAPI-75ee585f-3575-4d9a-8fcd-6421493b657a'

match_url = 'https://americas.api.riotgames.com/lol/match/v5/matches/'
timeline = '/timeline'

TOP = 'TOP'
JNG = 'JUNGLE'
MID = 'MIDDLE'
ADC = 'BOTTOM'
SUP = 'UTILITY'

## Sep 23
start_date = 1632380400
## Oct 4
end_date = 1633330800

matchdf = pd.read_csv('matches.csv')

invalid = []

def parseTimelineData(match_id, frame, row):
    result = [[], [], [], [], []]

    for i in range(5):
        result[i].append(int(row[i]))
        result[i].append(int(row[i+5]))
        result[i].append(i)
        result[i].append(frame[str(i+1)]['totalGold'] - frame[str(i+6)]['totalGold'])
        result[i].append(frame[str(i+1)]['xp'] - frame[str(i+6)]['xp'])
        result[i].append(match_id)
        
    return result

def getTimelineById(match_id, row):
    try:
        timeline_data = requests.get(match_url + match_id + timeline + '?' + api_key, timeout = 5).json()

        frames = timeline_data['info']['frames']

        if len(frames) >= 16:
            frame = frames[15]
        else:
            frame = frames[-1]

        return parseTimelineData(match_id, frame['participantFrames'], row)
    except Exception as e:
        print(match_id)
        invalid.append(match_id)
        print(e)
        return []

def main():
    with open('golddiff.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(['player 1', 'player 2', 'position', 'gold diff', 'xp diff', 'match id'])

        for idx, row in matchdf.iterrows():
            result = getTimelineById(row[11], matchdf.iloc[idx])

            if result != []:
                for i in result:
                    csvwriter.writerow(i)
            
                if (idx+1) / 80 == (idx+1) // 80:
                    print('current row count:', idx)
                    time.sleep(120)
    print(invalid)


main()
