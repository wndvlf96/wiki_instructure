# Cyberspace, Contents 등 특정 단어들을 통해서 sub뽑아서 security들 찾기.
# 특정 단어들 하나하나 반복문
# 반복문 안에서 BFS를 통해 탐색? 만약 트리가 아니라 순환고리가 있다면?(visit이 몇개인지도 모름..)

from collections import deque
import networkx as nx
import matplotlib.pyplot as plt
import json
import requests
import pydot
from networkx.drawing.nx_pydot import graphviz_layout
#import scipy

S = requests.Session()
URL = "https://en.wikipedia.org/w/api.php"
file = open("wiki_categories_Contents.txt", "w",encoding='UTF-8')
deq = deque([])
visit = ['Cyberwarfare','Contents', 'Films about computer hacking']


# 컨트롤h를 통해서 바꿀 카테고리 키워드 모두 바꿔주기!
# 결과 그림을 보고 뺄 키워드(subcategory) 여기 리스트에 넣기!
donotvisit = ['Malware in fiction','Hacking video games', 'Fictional hackers', 'Cryptography in fiction']

graph = nx.DiGraph()
# deq에 들어갈 친구 넣기(내가 생각하는 root친구들!)
#deq.append('Cyberwarfare')
deq.append(['Contents', 30, 0])
i=0
prev_height = 31
cur_col = 0
temp_height = 0
pos = {'Contents': [15,80]}
while deq:
    i+=1
    cur_node, cur_height, level = deq.popleft()
    print(i, cur_node)
    
    if prev_height == cur_height:
        cur_col += 2
    
    else:
        cur_col = 0
        temp_height = 0
        prev_height = cur_height

    file.write(cur_node)
    file.write('\n')
    category = "Category: "
    parentcate = cur_node
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
    graph.add_node(cur_node)

    for page in PAGES:


        subcat = page['title'][9:]
        if subcat not in donotvisit:
            cur_col += 800
            temp_height = temp_height - 3
            
            # 여기서 category: 이거는 떼자!
            # 문자열형식 예시: category:Socialists
            
            # 원래 있던 노드라면?!?! -> 알아서 위에 덮어써진다! 하지만 kind문제???
            # 근데 이 때 부모가 하나가 아니라면?!?!
            
            
            graph.add_node(subcat)
            graph.add_edge(cur_node, subcat)
            if subcat not in pos:
                pos[subcat] = [cur_col, cur_height - temp_height]

            # 근데 deq에 subcat넣기전에 visit확인하기!
            if subcat not in visit:
                if level < 3:
                    deq.append([subcat, cur_height-50, level+10])
                    visit.append(subcat)

g_dict = nx.node_link_data(graph)
g_dict_json = json.dumps(g_dict, indent=4)
file.close()
with open("wiki_cat_graph_Contents.json", "w") as outfile:
    json.dump(g_dict_json, outfile)

plt.figure(figsize=(30,30))
nx.draw_networkx_labels(graph, pos, font_size=8)
nx.draw_networkx_nodes(graph, pos, node_size = 5)
nx.draw_networkx_edges(graph, pos, alpha=0.2)
#nx.draw(graph, pos, font_size = 10, node_size = 5,font_color = 'blue', with_labels=True)
plt.savefig("Contents_cat.svg")
plt.show()
# https://www.mediawiki.org/wiki/API:Categorymembers
# https://en.wikipedia.org/w/api.php?action=query&list=categorymembers&cmtitle=Category:Computer%20security%20exploits&cmlimit=20
# 위 2개의 url을 조합한 코드를 통해서 카테고리에 대한 pages 얻을 수 있습니다.