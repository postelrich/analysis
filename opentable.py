import pandas as pd
import requests
import time


def get_restaurants(page=1):
    params = {'city': 'New York', 'per_page': 100, 'page': page}
    return requests.get('https://opentable.herokuapp.com/api/restaurants', params=params).json()['restaurants']


def get_all_restaurants():
    restaurants = dict()
    for i in range(1, 9999):
        print("  Getting restaurants page:", i)
        rs = get_restaurants(page=i)
        if not rs:
            return list(restaurants.values())
        restaurants.update({r['id']: r for r in rs})
        time.sleep(1)

def get_reviews(rid, page=1):
    r = requests.get(
        "https://oc-registry.opentable.com/v2/oc-reviews-listings/^1.0.1",
        params={'rid': rid, 'culture': 'en-us', 'page': page},
        headers={'Accept': 'application/vnd.oc.unrendered+json'}
    )
    return r.json()['data']['reviews']


def format_review(rid, r):
    r['restaurant_id'] = rid
    rating = r.pop('rating')
    for k, v in rating.items():
        r[k + '_rating'] = v
    reviewer = r.pop('reviewer')
    for k, v in reviewer.items():
        r[k + '_reviewer'] = v
    if r['diningOccasion']:
        r['dining_occasion'] = r['diningOccasion']['Id']
    for k in ['dateDinedDescription', 'helpfulness', 'helpfulnessCount',
              'lang', 'proTags', 'showTranslate', 'diningOccasion']:
        del r[k]
    return r


def get_all_reviews(rid):
    rs = dict()
    for i in range(1, 10):
        reviews = get_reviews(rid, i)
        if not reviews:
            return list(reviews.values())
        rs.update({r['reviewId']: format_review(rid, r) for r in reviews})
        time.sleep(0.1)
    return list(reviews.values())


def main():
    print("Getting all restaurants...")
    restaurants = get_all_restaurants()
    print("Number of restaurants:", len(restaurants))
    all_reviews = []
    for restaurant in restaurants:
        print("Getting reviews for:", restaurant['id'])
        reviews = get_all_reviews(restaurant['id'])
        print("  Number of reviews:", len(reviews))
        all_reviews.append(reviews)
    print("Total reviews retrieved:", len(all_reviews))
    print("Writing restaurants...")
    pd.DataFrame(restaurants).to_csv('data/ot_restaurants.csv')
    print("Writing reviews...")
    pd.DataFrame(all_reviews).to_csv('data/ot_reviews.csv')
    print("Done!")


if __name__ == '__main__':
    main()
