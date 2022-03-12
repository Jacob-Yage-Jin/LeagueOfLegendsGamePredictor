from riotwatcher import LolWatcher
import csv

'http://ddragon.leagueoflegends.com/cdn/11.20.1/data/en_US/champion.json'

## get the latest champion id and name, and write it to csv
def writeChampionDataToCsv():

    lol_watcher = LolWatcher('API-KEY')
    my_region = 'na1'
    versions = lol_watcher.data_dragon.versions_for_region(my_region)
    champions_version = versions['n']['champion']

    current_champ_list = lol_watcher.data_dragon.champions(champions_version)

    with open('champions.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(['id', 'name'])

        for champData in current_champ_list['data'].values():
            csvwriter.writerow([champData['key'], champData['name']])
    
