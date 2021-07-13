import requests

S = requests.Session()

URL = "https://en.wikipedia.org/w/api.php"

PARAMS = {
    "action":"query",
    "format": "json",
    "list":"categorymembers",   # 
    "cmtitle":"Category:malware",   # 
    "cmtype":"subcat",      # get recent category items
    "cmsort":"timestamp",   # 시간순으로
    "cmdir":"desc",         # ㅅ
    "cmlimit":"20"          # 20개
}

R = S.get(url=URL, params=PARAMS)
DATA = R.json()
print(DATA)
PAGES = DATA["query"]["categorymembers"]

for page in PAGES:
    print(page)