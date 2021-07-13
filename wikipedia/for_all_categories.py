"""
    get_allcategories.py

    MediaWiki API Demos
    Demo of `Allcategories` module: Get all categories, starting from a
    certain point, as ordered by category title.

    MIT License
"""

import requests

S = requests.Session()

URL = "https://en.wikipedia.org/w/api.php"
nextStr = ""
prevStr = "z"
file = open("wiki_categories.txt", "w",encoding='UTF-8')
# 반복을 언제까지 해야할까?
# nextStr이 z다음에 어떻게 될까?(Str의 변화가 없을때 반복문 그만!)
while True:
    if nextStr == prevStr:
        break
    PARAMS = {
        "action": "query",
        "format": "json",
        "list": "allcategories",
        "acfrom": nextStr,
        "aclimit":500       # 아무리 높게해도 최대 500으로 고정된다.
    }

    R = S.get(url=URL, params=PARAMS)
    DATA = R.json()
    CATEGORIES = DATA["query"]["allcategories"]
    num = 0
    for cat in CATEGORIES:
        # 여기서 print대신 txt에 써주기
        # 이 때 조건 있음: 처음 nextStr이 ""일 때를 제외하고는 맨 처음 것이 겹친다!
        if nextStr == "":
            file.writelines(cat["*"])
            file.write("\n")
        else:
            if num == 0:
                num += 1
                pass
            else:
                file.writelines(cat["*"])
                file.write("\n")
    
    prevStr = nextStr
    nextStr = CATEGORIES[-1]["*"]

file.close()