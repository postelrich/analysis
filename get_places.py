import json
import requests
import time
from tqdm import tqdm


COORDS = None
URL = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
DETAILS_URL = "https://maps.googleapis.com/maps/api/place/details/json"
RESTAURANTS = dict()
API_KEY = 'AIzaSyCRc8g_Kk6VE6b47qwecFNg6y-_ImX5E20'


def load_coords(path):
    global COORDS
    with open(path, 'r') as f:
        ll = f.readlines()
    COORDS = iter(ll)


def get_restaurants(next_token=None):
    if next_token:
        params = {'pagetoken': next_token,
                  'key': API_KEY}
    else:
        try:
            coord = next(COORDS)
            coord = coord.strip()
            print("COORD:", coord)
        except StopIteration:
            return
        params = {'key': API_KEY,
                  'location': coord,
                  'keyword': 'restaurant',
                  'radius': 1000}

    r = requests.get(URL, params)
    if not r.ok:
        get_restaurants()

    data = r.json()
    print("\tSTATUS:", data['status'], ", RESTAURANTS FOUND:", len(data['results']))
    for r in data['results']:
        RESTAURANTS[r['id']] = r
    if 'next_page_token' in data and data['next_page_token']:
        print("    NEXT PAGE")
        time.sleep(2)  # need to wait for next_page_token to validate on google server
        get_restaurants(data['next_page_token'])
    else:
        get_restaurants()


def places_main():
    load_coords('data/nyc-lat-lot.csv')
    get_restaurants()
    with open('data/restaurants.json', 'w') as f:
        json.dump(RESTAURANTS, f)


def load_places(path):
    with open(path, 'r') as f:
        data = json.load(f)
    return data


def get_reviews(restaurants):
    results = []
    for restaurant in tqdm(restaurants): #.values()):
        # print("ID:", restaurant['place_id'])
        params = {'key': API_KEY, 'placeid': restaurant['place_id']}
        r = requests.get(DETAILS_URL, params)
        if not r.ok:
            try:
                print(r.json())
            except:
                print(r.text())
        data = r.json()
        res = data.get('result')
        if res:
            results.append(res)
        else:
            print("\t", data)
    return results


def reviews_main():
    restaurants = load_places('data/restaurants.json')
    reviews = get_reviews(restaurants)
    with open('data/reviews.json', 'w') as f:
        json.dump(reviews, f)

if __name__ == '__main__':
    reviews_main()
