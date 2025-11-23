# 29559
import csv
import requests
import os
import xml.etree.ElementTree as ET
from dotenv import load_dotenv
import html
import time

load_dotenv()
bearer = os.getenv('BEARER_TOKEN')

# read csv file and filter records with rank 0
all_id = []
with open('boardgames_ranks.csv', encoding='utf-8') as f:
#with open('./top10.csv') as f:
    csv_reader = csv.reader(f)
    next(csv_reader)

    for row in csv_reader:
        id = row[0]
        rank = row[3]
        #print(rank)

        if rank != "0":
            all_id.append(id)

# print(all_id)

# split all_id list into batches of 20 (BGG limit)
split_list = [all_id[i:i+20] for i in range(0, len(all_id), 20)]
print(len(split_list))

# create output.csv file and add headers
with open('output.csv', mode = 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['id', 'name', 'rank', 'description', 'yearpublished', 'minplayers', 'maxplayers', 'playingtime', 'minplaytime', 'maxplaytime', 'minage', 'usersrated', 'average', 'owned', 'averageweight'])

#create categories.csv file and add headers
with open('categories.csv', mode = 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['id', 'category'])

#create mechanics.csv file and add headers
with open('mechanics.csv', mode = 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['id', 'mechanic'])


# join a batch into 1 string with ","
for i in split_list:
    id = ','.join(i)
    url = f'https://boardgamegeek.com/xmlapi2/thing?id={id}&stats=1'
    
    #add bearer token
    headers = {
        'Authorization': f'Bearer {bearer}'
    }
    #print(headers)

    response = requests.get(url, headers=headers)
    #print(response)

    #parse xml
    root = ET.fromstring(response.content)

    #get data
    for item in root.findall('item'):
        get_id = item.get('id')
        primary_name = ''
        for name in item.findall('name'):
            if name.get('type') == 'primary':
                primary_name = name.get('value', '')
                break
        # get_description = item.get('description')
        # get_yearpublished = item.get('yearpublished')
        # get_minplayers = item.get('minplayers')
        # get_maxplayers = item.get('maxplayers')
        # get_playingtime = item.get('playingtime')
        # get_minplaytime = item.get('minplaytime')
        # get_maxplaytime = item.get('maxplaytime')
        # get_minage = item.get('minage')
        # get_usersrated = item.get('usersrated')
        # get_average = item.get('average')
        # get_owned = item.get('owned')
        # get_averageweight = item.get('averageweight')
        desc_elem = item.find('description')
        if desc_elem is not None and desc_elem.text:
            #remove HTML entities
            get_description = html.unescape(desc_elem.text)
            get_description = ' '.join(get_description.split()) 
        else:
            get_description = ''
        
        year_elem = item.find('yearpublished')
        get_yearpublished = year_elem.get('value', '') if year_elem is not None else ''
        
        minp_elem = item.find('minplayers')
        get_minplayers = minp_elem.get('value', '') if minp_elem is not None else ''
        
        maxp_elem = item.find('maxplayers')
        get_maxplayers = maxp_elem.get('value', '') if maxp_elem is not None else ''
        
        playtime_elem = item.find('playingtime')
        get_playingtime = playtime_elem.get('value', '') if playtime_elem is not None else ''
        
        minplaytime_elem = item.find('minplaytime')
        get_minplaytime = minplaytime_elem.get('value', '') if minplaytime_elem is not None else ''
        
        maxplaytime_elem = item.find('maxplaytime')
        get_maxplaytime = maxplaytime_elem.get('value', '') if maxplaytime_elem is not None else ''
        
        age_elem = item.find('minage')
        get_minage = age_elem.get('value', '') if age_elem is not None else ''
        
        stats = item.find('.//ratings')
        if stats is not None:
            rated_elem = stats.find('usersrated')
            get_usersrated = rated_elem.get('value', '') if rated_elem is not None else ''
            
            avg_elem = stats.find('average')
            get_average = avg_elem.get('value', '') if avg_elem is not None else ''
            
            owned_elem = stats.find('owned')
            get_owned = owned_elem.get('value', '') if owned_elem is not None else ''
            
            weight_elem = stats.find('averageweight')
            get_averageweight = weight_elem.get('value', '') if weight_elem is not None else ''
        else:
            get_usersrated = get_average = get_owned = get_averageweight = ''

        ranks = item.find('.//ranks')
        rank_id = ''
        if ranks is not None:
            for rank in ranks.findall('rank'):
                if rank.get('type') == 'subtype':
                    rank_id = rank.get('value', '')
                    break

        
        #save data to dictionary
        data = {
            'id': get_id,
            'name': primary_name,
            'rank': rank_id,
            'description': get_description,
            'yearpublished': get_yearpublished,
            'minplayers': get_minplayers,
            'maxplayers': get_maxplayers,
            'playingtime': get_playingtime,
            'minplaytime': get_minplaytime,
            'maxplaytime': get_maxplaytime,
            'minage': get_minage,
            'usersrated': get_usersrated,
            'average': get_average,
            'owned': get_owned,
            'averageweight': get_averageweight
        }

        #open output.csv and save dictionary to csv
        with open('output.csv', mode = 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(data.values())

        #open categories.csv and append values
        for link in item.findall("link[@type='boardgamecategory']"):
            category_name = link.get('value')
            with open('categories.csv', mode = 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([get_id, category_name])

        #open mechanics.csv and append values
        for link in item.findall("link[@type='boardgamemechanic']"):
            mechanic_name = link.get('value')
            with open('mechanics.csv', mode = 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([get_id, mechanic_name])

    # Pause 5s to avoid hitting BGG rate limits
    time.sleep(5)

print('Finish')