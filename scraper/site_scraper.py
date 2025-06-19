from typing import Any
import requests
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup
from typing import Dict
import re
import json

from config import DECKLISTS_URL, BASE_URL, TEST_URL

# --- TO DOs ---
# 1. save off tournament raw data
# 2. filter tournaments by challenge/league and/or format
# 3. add logging
# 4. Retry() from urllib3
# 5. Classes?

def create_session(retries: int = 5) -> requests.Session:
    session = requests.Session()
    adapter = HTTPAdapter(max_retries=retries)
    session.mount('https://', adapter)
    session.mount('http://', adapter)
    return session

def fetch_page(session: requests.Session, url: str) -> bytes:
        response = session.get(url, timeout=10)
        response.raise_for_status()
        return response.content

def parse_tournaments(html_content: bytes) -> list[Dict]:
    soup = BeautifulSoup(html_content, 'html.parser')
        
    container = soup.find('ul', class_='decklists-list')
    items = container.find_all('li', class_='decklists-item')
    tournaments = []
    for item in items:
        tournaments.append({
            'href': item.find('a')['href'].strip(),
            'name': item.find('h3').text.strip(),
            'datetime': item.find('time')['datetime'].strip()
        })
    return tournaments

def parse_single_tournament(html_content: bytes):
    soup = BeautifulSoup(html_content, 'html.parser')

    for script in soup.find_all('script'):
        script_text = script.get_text()
        if 'window.MTGO.decklists.data' in script_text:
            target_script = script_text

    match = re.search(r'window\.MTGO\.decklists\.data\s*=\s*(\{.*?\});', target_script, re.DOTALL)
    json_str = match.group(1)

    data = json.loads(json_str)

    print(data)
    

def main():

    session = create_session()

    try:
        html = fetch_page(session, DECKLISTS_URL)
        tournaments = parse_tournaments(html)

        test_html = fetch_page(session, TEST_URL)
        decklists = parse_single_tournament(test_html)

        # for tournament in tournaments:
            #  tournament_url = BASE_URL + tournament['href']


    except Exception as e:
        print(f'Error: {e}')

if __name__ == '__main__':
    main()