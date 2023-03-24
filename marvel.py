import requests
import hashlib
import pandas as pd

public_key = ''
private_key = ''
endpoint = 'https://gateway.marvel.com/v1/public/characters'

timestamp = '1'  
hash_input = timestamp + private_key + public_key
hash_output = hashlib.md5(hash_input.encode('utf-8')).hexdigest()

params = {
    'ts': timestamp,
    'apikey': public_key,
    'hash': hash_output,
    'limit': 100  
}


characters = []

while True:
    response = requests.get(endpoint, params=params)
    data = response.json()['data']['results']
    
    for character in data:
        char_id = character['id']
        name = character['name']
        description = character['description']
        comics = character['comics']['available']
        series = character['series']['available']
        stories = character['stories']['available']
        events = character['events']['available']
        
        characters.append({
            'id': char_id,
            'name': name,
            'description': description,
            'comics': comics,
            'series': series,
            'stories': stories,
            'events': events
        })
   
    if len(data) < params['limit']:
        break
        
    params['offset'] = params.get('offset', 0) + params['limit']

df = pd.DataFrame(characters)

df.to_csv('marvel.csv', index=False)
