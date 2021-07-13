from urllib.request import urlopen
from bs4 import BeautifulSoup
import os
import re
import json

# https://en.wikipedia.org/wiki/Stalkerware
# 어떤 카테고리를 넣으면 wikipedia에서 그 카테고리에 해당하는 모든 Page들의 html다운받기(content의 text단 정도?)

category = "Stalkerware"
html = urlopen("https://en.wikipedia.org/wiki/Category:"+category)
bsObj = BeautifulSoup(html, "html.parser")

# 해당 html의 Page들 부분
mw_pages = bsObj.find(attrs={'id':'mw-pages'})

pages = mw_pages.find(attrs={'class':'mw-category'})
if pages == None:
    mw_contents = mw_pages.find(attrs={'class':'mw-content-ltr'})
    pagesUrl = mw_contents.find_all('a')
else:
    pagesUrl = pages.find_all('a')
for pageurl in pagesUrl:
    # 해당 html에서 각 page들 접근
    url = 'https://en.wikipedia.org'+pageurl.get('href')

    # 각 text 수집
    html = urlopen(url)
    bsObj_page = BeautifulSoup(html, "html.parser")
    contents = bsObj_page.find(attrs={'class':'mw-parser-output'})

    # 각 html 저장하기
    nm = str(pageurl.get('href')).split('/')[2]
    # nm안에 디렉토리명으로 불가능한 문자가 있을 경우를 대비
    # \ / : * ? " < > | 이렇게 있음
    if (':' in nm) or ('\\' in nm) or ('/' in nm) or ('*'in nm) or ('?' in nm) or ('\"' in nm) or ('<' in nm) or ('>' in nm) or ('|' in nm):
        nm = nm.replace(':','(colon)')
        nm = nm.replace('\\','(backslash)')
        nm = nm.replace('/','(slash)')
        nm = nm.replace('*','(star)')
        nm = nm.replace('?','(question_mark)')
        nm = nm.replace('\"','(double_quotation_mark)')
        nm = nm.replace('<','(r_inequality_sign)')
        nm = nm.replace('>','(l_inequality_sign)')
        nm = nm.replace('|','(bar)')
    
    print(nm)

    # 폴더 없으면 폴더 만들기
    try:
        if not os.path.exists("D:\wikipedia_crawl\_"+category+"_"):
            os.makedirs("D:\wikipedia_crawl\_"+category+"_")
    except OSError:
        print("error")

    file = open("D:\wikipedia_crawl\_"+category+"_\wikipedia"+"_"+category+"_"+nm+".txt", "w",encoding='UTF-8')

    # 형식: 
    # 1. 페이지 제목
    # 2. P 태그로 내용
    # 3. h2 있다면 그걸로 소제목
    # 3.5: h3가 있을수도...
    # 4. 소제목의 내용(여러 단락으로 이루어져있을 경우 한 소제목에 p태그 여러개일수도...)(ul태그일수도)
    # 3,4 반복
    
    #content = contents.find_all({'div','h2','h3','p','ul','ol'})
    content = contents
    '''
    content = contents.text
    content = content.replace('\n\n','\n')
    content = content.replace('\n\n','\n')
    content = content.replace('\n\n','\n')
    content = content.replace('\n\n','\n')
    content = content.replace('\n\n','\n')
    content = content.replace('\n\n','\n')
    
    file.write(nm+' of '+ category+'\n\n')
    file.write(content)

    '''
    file.write(nm+' of '+ category+'\n\n')


    json_object={}
    json_object["name"] = nm
    sub = {}
    ssub = {}
    cont = []
    for i in content.children:
        if str(i)[0] != '<' or str(i)[0:6] == '<table' or str(i)[0:12] == "<div aria-la" or str(i)[0:6] == '<style':
            # 주석이나 table이면 넘어가기 위해서
            continue
        
        

        # h2일때
        if str(i)[0:4] == '<h2>':
            if ssub == {}:
                if not sub and len(cont) > 0:
                    json_object["content"] = cont
                    cont = []
                elif sub and len(cont) > 0:
                    sub["content"] = cont
                    json_object[sub["name"]] = sub
                    sub = {}
                    cont = []
            else:
                sub[ssub["name"]] = ssub
            i = re.sub('<.+?>', '', str(i), 0).strip()
            i = i.replace('[edit]','')
            sub["name"] = i
        # h3일때
        elif str(i)[0:4] == '<h3>':
            if ssub:
                ssub["content"] = cont
                cont = []
                ssub = {}
            i = re.sub('<.+?>', '', str(i), 0).strip()
            i = i.replace('[edit]','')
            ssub["name"] = i

        # 내용일때
        else:
            i = re.sub('<.+?>', '', str(i), 0).strip()
            cont.append(i)


        file.write(str(i)+'\n')
        #i = re.sub('<.+?>', '', str(i), 0).strip()
        

    
    # 내용으로 끝난 이후에!
    json_object[sub["name"]] = sub
    with open("D:\wikipedia_crawl\_"+category+"_\wikipedia"+"_"+category+"_"+nm+".json", 'w') as f:
        json.dump(json_object, f, indent="\t")

    file.close()