# 카테고리 적혀있는 거에 대해서 pages들 url 저장하기
import requests

S = requests.Session()

URL = "https://en.wikipedia.org/w/api.php"
category = "Computer security exploits"
PARAMS = {
    "format": "json",
    "list": "categorymembers",
    "action": "query",
    "cmtitle": "Category:"+category,
    "cmlimit": 20
}

R = S.get(url=URL, params=PARAMS)
DATA = R.json()
PAGES = DATA["query"]["categorymembers"]
f = open("pages for "+category+".txt", 'w', encoding='UTF-8')
for page in PAGES:
    f.write("https://en.wikipedia.org/wiki/" + page["title"])
    f.write('\n')
    print("https://en.wikipedia.org/wiki/" + page["title"])
f.close()