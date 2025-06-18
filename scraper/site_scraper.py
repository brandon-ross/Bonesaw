from typing import Any
import requests
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup
from typing import Dict

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

def main():

    session = create_session()

    try:
        html = fetch_page(session, 'https://www.mtgo.com/decklists')
        tournaments = parse_tournaments(html)
        for t in tournaments:
             print(t)

    except Exception as e:
        print(f'Error: {e}')

if __name__ == '__main__':
    main()