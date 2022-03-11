import requests
import csv
import time

api_key = 'api_key=RGAPI-4f4e680d-edd2-4202-8f74-12026cc61bc5'

match_url = 'https://americas.api.riotgames.com/lol/match/v5/matches/'

TOP = 'TOP'
JNG = 'JUNGLE'
MID = 'MIDDLE'
ADC = 'BOTTOM'
SUP = 'UTILITY'

## Sep 23
start_date = 1632380400
## Oct 4
end_date = 1633330800

start_player = 'ovbrntTQqIz3efVZ5_qW0OwNJi4yCgp8eUmiKq8Syg6aEz66opxJ8S_n2cIycUFoF51Ntqvekt87gA'

players_lst = [start_player]
players_visited = {}
players_visited[start_player] = True

match_visited = {}

row_count = 0

def parseMatchData(players):
    result = [''] * 5

    for player_data in players:
        puuid = player_data['puuid']
        if puuid not in players_visited:
            players_lst.append(puuid)
            players_visited[puuid] = True
            
        position = player_data['teamPosition']
        champion = player_data['championId']
        if position == TOP:
            result[0] = champion
        elif position == JNG:
            result[1] = champion
        elif position == MID:
            result[2] = champion
        elif position == ADC:
            result[3] = champion
        else:
            result[4] = champion

    return result

def getMatchResultById(match_id):
    return_value = []

    try:
        match_data = requests.get(match_url + match_id + '?' + api_key, timeout = 5).json()

        player_data = match_data['info']['participants']

        return_value += parseMatchData(player_data[:5])
        return_value += parseMatchData(player_data[5:])

        result = match_data['info']['teams']
        return_value.append('blue' if result[0]['win'] else 'red')
        return_value.append(match_id)
    except Exception as e:
        print(e)

    return return_value

def getMatchHistoryById(player_id, csvwriter):
    global row_count

    try:    
        match_data = requests.get(match_url + 'by-puuid/' + player_id + '/ids' + '?startTime=' + str(start_date) + '&endTime=' + str(end_date) + '&queue=420&type=ranked&count=100&' + api_key, timeout = 5).json()
    except Exception as e:
        print(e)
        match_data = []

    for match_id in match_data:
        if match_id not in match_visited:
            match_visited[match_id] = True

            match_result = getMatchResultById(match_id)

            if match_result != []:
                csvwriter.writerow(match_result)

                row_count += 1

                if row_count / 70 == row_count // 70:
                    print('current row count:', row_count)
                    time.sleep(120)
            

def main():    
    with open('matches.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(['blue top', 'blue jungle', 'blue mid', 'blue adc', 'blue sup', 'red top', 'red jungle', 'red mid', 'red adc', 'red sup', 'match result', 'match id'])

        for player_id in players_lst:
            getMatchHistoryById(player_id, csvwriter)

            if row_count >= 10000:
                return

main()
