import re

import requests
import urllib3.exceptions
from bs4 import BeautifulSoup
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_news():
    result = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
    }
    url = "https://bdu.fstec.ru/vul/"
    response = requests.get(url, verify=False, headers=headers)
    found = False
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")

        target_text = "Последние изменения"  # Text to search for

        region_of_interest = None

        for text in soup.find_all(string=True):
            if target_text in text:
                region_of_interest = text.find_parent("div")
                found = True
                break

    if found:
        target = region_of_interest.find_next()
        target_links = target.find_all("a", href=True)
        for i in target_links:
            vul_id = re.findall(r'vul/(.*?)\"', str(i))[0]
            text = i.text
            result.append((vul_id, text))
    return result


def get_list_of_useful_news(components):
    result = []
    news = get_news()
    for component in components:
        for new in news:
            if component.lower() in new[1].lower():
                result.append(new)
    return result


if __name__ == "__main__":
    for i in get_news():
        print(i)
    print("*" * 30)
    for i in get_list_of_useful_news(['HP OfficeJet Pro', 'Artica Proxy']):
        print(i)
