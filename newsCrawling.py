from bs4 import BeautifulSoup
from selenium import webdriver
import time
import re
from openpyxl import Workbook


class Article:
    def __init__(self, title,time,url):
        self.title = title
        self.time = time
        self.url = url

    def print(self):
        print("제목:", self.title, ", 시간: ",self.time, ", 관련뉴스: ",self.related)

    def addRelated(self, num):
        self.related = num


write_wb = Workbook()
write_ws = write_wb.active #WorkSheet


#query_txt = input("크롤링할 키워드는 무엇입니까? : ")
query_txt = "안나푸르나"
#Step 1. 크롬 드라이버를 사용해서 웹 브라우저를 실행한다
path = "C:/Users/user/PythonProjects/chromedriver.exe"
driver = webdriver.Chrome(path)

driver.get("http://news.naver.com")
time.sleep(2) #위 페이지가 모두 열릴 때까지 2초 기다린다.

#Step 2. 검색창의 이름을 찾아서 검색어를 입력한다.
driver.find_element_by_class_name("text_index").click()#웹 페이지에서 해당 이름을 주고 클릭 시킨다.

element = driver.find_element_by_class_name("text_index")

element.send_keys(query_txt)#엘리멘트에 해당 키(검색어)를 준다.

#Step 3. 검색 버튼을 눌러 실행한다.
driver.find_element_by_xpath("/html/body/div/div[3]/div[3]/div/div/form/fieldset/button").click()

#-----------------------------

time.sleep(2)

driver.switch_to.window(driver.window_handles[-1])
driver.find_element_by_xpath("/html/body/div[3]/div[2]/div/div[1]/div[2]/div[1]/div[3]/ul/li[2]").click() #최신순

full_html = driver.page_source #현재 페이지의 모든 코드를 가져와라

soup = BeautifulSoup(full_html,"html.parser")#스프한테 분석시킨다.
content_list = []

#content_list = soup.find('ul').find_all('li')
for index, i in enumerate(soup.find('ul', {"class" : "type01"}).find_all('li',{"id":re.compile("sp_nws\d+")})):
    # <ul> 중에 id가 sp_nws로 시작하는 <li>만 모아서
    #Title 저장
    print(index,"번째,")
    try:
        title = i.find("a","_sp_each_title").get_text()
        print("title:",title)
    except AttributeError:
        print ("NO TITLE")
    
    #url
    url = i.find("a")["href"]
    print("url:",url)
    
    #time
    time_tag = str(i.find("dd",{"class":"txt_inline"})) #dd 텍스트형식으로 저장
    time_p = re.compile("\d+\w+\s전" or "\d{4}.\d{2}.\d{2}") #n시간 전 or n일 전 or  yyyy.mm.dd.
    time_str = time_p.findall(time_tag)
    print("time:",time_str[0])


    #relatedNews
    num_related = 0
    try:
        related = i.find("div",{"class":"newr_more"}).get_text()
        related_p = re.compile("\d+").findall(related) #숫자인거 따오기
        num_related = int(related_p[0])
        print("related news: ",num_related)
    except AttributeError:
        num_related = 0
        print("NO RELATED")

    #직접달린 연관뉴스들 더하기
    try:
        dir_related = i.find("ul",{"class":"relation_lst"}).findChildren("li")
        num_dir_related = len(dir_related)
        num_related += num_dir_related
        print("dir_related: ",num_dir_related,"개, 총: ", num_related)
    except AttributeError:
        print("NO DIRECT RELATED")

    temp = Article(title,time_str[0],url)
    temp.addRelated(num_related)
    content_list.append(temp)

print(len(content_list))
for i in content_list:
    i.print() #멤버함수임
    write_ws.append([i.title,i.time,i.url,i.related])

# for i in content_list : 
#    print(i.title)


#---------------------------

#표준 출력 장치(모니터), 표준 입력 장치(키보드)
#표준 출력 장치를 파일로 바꾼다.
import sys

orig_stdout = sys.stdout 
f = open("test.txt",'a',encoding="UTF=8")#워크스페이스에 생성된다.
sys.stdout = f
time.sleep(1)
#sys.stdout은 기본 출력 장치를 말한다.
#기본 출력 장치를 파일로 바꾼다.

# html = driver.page_source
# soup = BeautifulSoup(html,"html.parser")#스프한테 분석시킨다.
# content_list = soup.find('ul',class_='list_thumType flnon')

#for문에서의 print는 이제 파일로 들어간다.
for i in content_list:
    print(i)
    print('\n')

sys.stdout = orig_stdout # 표준 출력 장치 원상복구
f.close() # 파일 사용 후 반드시 닫아준다
print("완료")