import requests
import re
from bs4 import BeautifulSoup
import json


URL = 'https://www.vasttrafik.se/reseplanering/hallplatslista/'

html = requests.get(URL)


soup = BeautifulSoup(html.text, 'html.parser')

URL_dic = {}

#child_soup = soup.find_all('a', ('Zon A'))
for tag in soup.find_all("a", text=re.compile("Zon A.*")):
    stop = tag.string.splitlines()[1].lstrip()[:-1]
    codename = tag.get('href').replace('/reseplanering/hallplatser/', '')[:-1]
    final_URL = 'https://avgangstavla.vasttrafik.se/?source=vasttrafikse-stopareadetailspage&stopAreaGid=' + codename
    URL_dic[stop] = final_URL


file = open('URL.json', 'w', encoding = 'utf-8')
json.dump(URL_dic, file, indent=4, separators=None, ensure_ascii=False)
file.close()