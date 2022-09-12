import requests


def get_data(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
    except requests.exceptions.RequestException as err:
        raise Exception('Проблема с  API: ' % err)
    return r.text
