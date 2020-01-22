import requests #cmd에서 pip install해줘야함
from bs4 import BeautifulSoup
import datetime

query_txt = input("검색할 키워드 : ")
date_from_txt = input("검색 시작 날짜(ex, 2020.1.10) : ")#~현재까지
date_interval_txt = int(input("날짜 간격 : "))*10#기본은 1일

def loof(query_txt):
    current = datetime.datetime.now()
    index = datetime.datetime.now()

    flag = 0
    key = 1 #시간 변화용 변수
 
    while flag != 1:
        page = 1
        maxpage = 50#검색 범위 임의 지정 -> 5페이지
        pnum = 1
        year = current.year
        month = current.month
        day = current.day
        if date_from_txt == str(year)+'.'+str(month)+'.'+str(day) :# 날짜만큼 반복
            flag = 1
        while page < maxpage:
            url = 'https://search.naver.com/search.naver?&where=news&query='+query_txt.strip()+'&sm=tab_pge&sort=0&photo=0&field=0&reporter_article=&pd=0&ds='+str(year)+'.'+str(month)+'.'+str(day)+'&de='+str(year)+'.'+str(month)+'.'+str(day)+'&docid=&nso=so:r,p:all,a:all&mynews=0&start='+str(page)+'&refresh_start=0'
            page += 10
            response = requests.get(url=url)
            #print(response.status_code)#url을 정상적으로 받았으면 200을 출력
            if response.status_code == 200 :
                html = BeautifulSoup(response.text,'html.parser')
                tags = html.select('#main_pack > div.news.mynews.section._prs_nws > ul')[0].find_all('a')
                #select('찾으려는 태그의 위치').find_all(태그) 해당 위치의 동일한 태그를 모두 찾는다.
                #xpath처럼 복사하여 찾을 수 있다.
                if not tags:
                   return title_list, url_list
                else:
                    for tag in tags:
                        text = tag.text
                        href = tag['href']
                        if text!='보내기' and text!='네이버뉴스':
                            title_list.append(text)
                            url_list.append(href)

                pnum += int(date_interval_txt)
                print(pnum-1)
            else:
                return (title_list, url_list)
        current = index - datetime.timedelta(days = key)#목표하던 시간부터, 현재까지 하루씩 뺌
        key += 1

title_list = []#제목 리스트
url_list = []#url리스트

loof(query_txt)
print(title_list)
print(url_list)
print(len(title_list))
print(len(url_list))

