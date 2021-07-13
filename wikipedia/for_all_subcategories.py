# https://en.wikipedia.org/w/api.php?action=query&list=categorymembers&cmtitle=Category:Socialism&cmtype=subcat&cmlimit=200
# 위의 주소를 통해서 request로 받아오기!

import requests
import networkx as nx
import json
import matplotlib.pyplot as plt

S = requests.Session()
URL = "https://en.wikipedia.org/w/api.php"


# 여기부터 반복문으로 조지기
# 모든 카테고리 담은 파일 한줄씩 읽기
f = open("wiki_categories.txt", 'r', encoding='UTF-8')
graph = nx.DiGraph()
lines = f.readlines()
i=0
for line in lines:
    i=i+1
    print(i, line)
    
    
    category = "Category: "
    parentcate = line
    category = category + parentcate
    # print(i,category) -> 32 Category: "Weird Al" Yankovic images
    PARAMS = {
        "action": "query",
        "cmtitle": category,
        "cmtype": "subcat",
        "cmlimit": "500",
        "list": "categorymembers",
        "format": "json"
    }

    R = S.get(url=URL, params=PARAMS)
    DATA = R.json()
    PAGES = DATA['query']['categorymembers']
    graph.add_node(line)

    for page in PAGES:
        subcat = page['title'][9:]
        # 여기서 category: 이거는 떼자!
        # 문자열형식 예시: category:Socialists
        
        # 원래 있던 노드라면?!?! -> 알아서 위에 덮어써진다! 하지만 kind문제???
        # 근데 이 때 부모가 하나가 아니라면?!?!
        graph.add_node(subcat, kind=line)
        graph.add_edge(line,subcat)


f.close()
g_dict = nx.node_link_data(graph)
g_dict_json = json.dumps(g_dict, indent=4)
with open("wiki_cat_graph.json", "w") as outfile:
    json.dump(g_dict_json, outfile)
plt.figure(figsize=(30,30))
pos = nx.spring_layout(graph, k=0.1)
nx.draw(graph, pos, node_size = 15, with_labels=True)
plt.savefig("allcat.png")
plt.show()
