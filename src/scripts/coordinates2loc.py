import requests
import json

def coordinates2loc(lat, lng):
    API_KEY = '' << ADD KEY HERE
    GMAP_API_ENDPOINT = 'https://maps.googleapis.com/maps/api/geocode/json'
    url = f'{GMAP_API_ENDPOINT}?latlng={lat},{lng}&key={API_KEY}'
    print(f'Fetching URL[{url}]')
    r=requests.get(url)
    print(r.status_code)
    #print(str(r.content))
    data = json.loads(r.content)
    address_components = data.get('results')[0]['address_components']
    print(address_components)
    for item in address_components:
        if 'administrative_area_level_2' in item['types']:
            locality = item['long_name']
        if 'administrative_area_level_1' in item['types']:
            state = item['long_name']
    return (locality, state)

if __name__ == '__main__':
    lat = '15.4589'
    lng = '75.0078'
    (locality, state) = coordinates2loc(lat, lng)
    print(locality, state)
