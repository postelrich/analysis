import requests


def get_places(**kwargs):
    url = "https://api.foursquare.com/v2/venues/search"
    kwargs['client_id'] = '3BDM4BGF14QYWNQ5FOHULYUEIWQBTCYI5JTK53EL12R1ZYRW'
    kwargs['client_secret'] = 'FSMFOMCF40UHZVHZLUP42AUP4ECZORNOBEFLZKR0YVUJ0D1W'
    kwargs['categoryId'] = '4d4b7105d754a06374d81259'
    kwargs['limit'] = 50
    r = requests.get(url, kwargs)
    if not r.ok:
        raise requests.RequestException(r.text)
    return r.json()
