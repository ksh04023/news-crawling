import requests #cmd에서 pip install해줘야함
from bs4 import BeautifulSoup
import datetime
from datetime import timedelta
import re

query_txt = input("검색할 키워드 : ")
date_from_txt = input("검색 시작 날짜(ex, 2020.1.10) : ")#~현재까지

class Article:
    def __init__(self, title,time,url):
        self.title = title
        self.time = time
        self.url = url

    def print(self):
        print("제목:", self.title, ", 시간: ",self.time, ", 관련뉴스: ",self.related)

    def addRelated(self, num):
        self.related = num

content_list=[]
#과거 시점부터 크롤링을 시작하여 현재 시점까지 진행한다.
def article_search(query_txt):
    current = datetime.datetime.now()
    index = datetime.datetime.now()
    flag = 0
    key = 1 #뉴스 기사의 시점을 판단하기 위한 변수
    while flag != 1:
        page = 1
        maxpage = 50 #검색 범위 임의 지정 -> 5페이지, 숫자를 높일 경우 1일당 검색되는 기사의 양이 많아진다.
        #ㅇㅅㅇ? 우리가 원하는게 기사수가 얼마나 많은지 구하는건데 max를 정하는건가,,?
        year = current.year
        month = current.month
        day = current.day
        if date_from_txt == str(year)+'.'+str(month)+'.'+str(day) :# 현재 시점의 기사를 크롤링 할 경우 종료
            flag = 1
        while page < maxpage:
            url = 'https://search.naver.com/search.naver?&where=news&query='+query_txt.strip()+'&sm=tab_pge&sort=0&photo=0&field=0&reporter_article=&pd=0&ds='+str(year)+'.'+str(month)+'.'+str(day)+'&de='+str(year)+'.'+str(month)+'.'+str(day)+'&docid=&nso=so:r,p:all,a:all&mynews=0&start='+str(page)+'&refresh_start=0'
            #url중간 마다 검색 키워드, 날짜, 페이지가 입력된다.
            page += 10
            response = requests.get(url=url)
            #print(response.status_code)#url을 정상적으로 받았으면 200을 출력
            if response.status_code == 200 :
                html = BeautifulSoup(response.text,'html.parser')
                tags = html.select('#main_pack > div.news.mynews.section._prs_nws > ul')[0].find_all('li',{"id":re.compile("sp_nws\d+")})
                #select('찾으려는 태그의 위치').find_all(태그) 해당 위치의 동일한 태그를 모두 찾는다.
                #xpath처럼 복사하여 찾을 수 있다.
                if not tags:#태그가 존재하지 않을 경우 리스트 리턴
                   return content_list
                else:
                    for tag in tags: #이밑에거 함수로 넣을까말까~~
                        try:
                            title = tag.find("a","_sp_each_title").get_text()
                            print("title:",title)
                        except AttributeError:
                            print ("NO TITLE")
                        
                        #url
                        url = tag.find("a")["href"]
                        print("url:",url)
                        
                        #time
                        time_tag = str(tag.find("dd",{"class":"txt_inline"})) #dd 텍스트형식으로 저장
                        time = re.compile("\d+\w+\s전" or "\d{4}.\d{2}.\d{2}").findall(time_tag)[0] #n시간 전 or n일 전 or  yyyy.mm.dd.
                        time_obj = datetime.datetime.now()
                        sub = re.findall("\d+",time) #숫자만 추출
                        if "시간" in time:
                            time_obj -= timedelta(hours = int(sub[0])) #시간만큼 빼기
                            #print(sub,"시간", time_obj.strftime("%Y.%m.%d"))

                        elif "일" in time:
                            time_obj -= timedelta(days = int(sub[0])) #일만큼 빼기
                            #print(sub,"일", time_obj.strftime("%Y.%m.%d"))
                            
                        time_str = time_obj.strftime('%Y.%m.%d') #YYYY.mm.dd
                        print("time:",time,",",time_str)


                        #relatedNews
                        num_related = 0
                        try:
                            related = tag.find("div",{"class":"newr_more"}).get_text()
                            related_p = re.compile("\d+").findall(related) #숫자인거 따오기
                            num_related = int(related_p[0])
                            print("related news: ",num_related)
                        except AttributeError:
                            num_related = 0
                            print("NO RELATED")

                        #직접달린 연관뉴스들 더하기
                        try:
                            dir_related = tag.find("ul",{"class":"relation_lst"}).findChildren("li")
                            num_dir_related = len(dir_related)
                            num_related += num_dir_related
                            print("dir_related: ",num_dir_related,"개, 총: ", num_related)
                        except AttributeError:
                            print("NO DIRECTLY RELATED")

                        temp = Article(title,time_str,url)
                        temp.addRelated(num_related)
                        content_list.append(temp)

                    # print(len(content_list))
                    # for i in content_list:
                    #     i.print() #멤버함수임
                        
            else:
                return content_list #정상적으로 url을 받지 못했다면 리턴
        current = index - datetime.timedelta(days = key)#목표하던 시간부터, 현재까지 하루씩 뺌 timedelta -> 날짜연산
        key += 1

def sort_by_time(content_list):
    content_sorted = sorted(content_list, key = lambda Article: Article.time)
    for i in content_sorted:
        i.print()

# title_list = []#제목 리스트
# url_list = []#url리스트
content_list = []
article_search(query_txt)
print("길이",len(content_list))
sort_by_time(content_list)

