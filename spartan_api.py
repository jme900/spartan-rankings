import requests
import re
from spartan_db import insert_ag_rankings, insert_elite_rankings

HEADERS = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip,deflate,utf-8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
                  'like Gecko) Chrome/115.0.0.0 Safari/537.36'
}


def _replace_url_params(url, page_size, start_at_index):
    if "page_size=" in url:
        url = re.sub(r"(?<=page_size=)\d+", str(page_size), url)
    else:
        url += "&page_size=" + str(page_size)
    if "start_at_index=" in url:
        url = re.sub(r"(?<=start_at_index=)\d+", str(start_at_index), url)
    else:
        url += "&start_at_index=" + str(start_at_index)
    return url


def save_rankings_from_api(url, series, race_name, start_index=0):
    print(f"Crawling results for: {race_name} - index:{start_index}")
    if start_index is not None:
        url = _replace_url_params(url, 50, int(start_index))
        print(f"api: {url}")
        try:
            response = requests.get(url, headers=HEADERS)
            results = response.json()
            start_index = results.get("next_index")
            rankings = results.get("rankings", [])
            if len(rankings) > 0:
                insert_ag_rankings(series, race_name, rankings)
            save_rankings_from_api(url, series, race_name, start_index)
        except Exception as e:
            print(e)


def save_elite_rankings_from_api(url, series, race_name, start_index=0):
    print(f"Crawling elite results for: {race_name} - index:{start_index}")
    if start_index is not None:
        url = _replace_url_params(url, 50, int(start_index))
        print(f"api: {url}")
        try:
            response = requests.get(url, headers=HEADERS)
            results = response.json()
            start_index = results.get("next_index")
            rankings = results.get("rankings", [])
            if len(rankings) > 0:
                insert_elite_rankings(series, race_name, rankings)
            save_elite_rankings_from_api(url, series, race_name, start_index)
        except Exception as e:
            print(e)
