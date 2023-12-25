#con

from selenium import webdriver
from selenium.webdriver.common.by import By   
from selenium.webdriver.chrome.options import Options
import time, random, os, webbrowser, pandas as pd

options = Options()
options.add_argument("--start-maximized") 
options.add_argument("--headless=new") 
options.add_experimental_option("detach", True) 

d = webdriver.Chrome(options=options)
time.sleep (3)

start = print("●Starting Google Store APP Review Scraper●")

app_name = input("〓▶App 이름은 무엇인가요? : ")
print("====Google Store 홈페이지가 열립니다.=====")
time.sleep (3)
google_store = f'https://play.google.com/store/search?q={app_name}=apps&hl=ko&gl=US'
webbrowser.open_new(google_store)
app_url = input("〓▶원하시는 APP을 클릭하신 후 해당페이지의 URL을 입력해주세요 : ")
numbers = int(input("〓▶리뷰를 몇개 정도 가져올까요?\n(!각 리뷰의 길이에 따라 총개수는 달라질 수 있습니다!): "))
scroll = int(numbers/45)
now = time.localtime()
date_format = '%04d%02d%02d'%(now.tm_year, now.tm_mon, now.tm_mday)
f_dir = f'{os.getcwd()}'

#test용###
#app_url = "https://play.google.com/store/apps/details?id=com.ilevit.alwayz.android&hl=ko-KR"
#app_name= 'test'
#scroll = 10
#####

d.get(app_url)

time.sleep(random.randint(3,5))

#더보기 클릭 열기
moer ='//*[@id="yDmH0d"]/c-wiz[2]/div/div/div[2]/div[2]/div/div[1]/div[1]/c-wiz[4]/section/div/div[2]/div[5]/div/div/button/span'
d.find_element(By.XPATH, moer).click()
#moer.send_keys(Keys.ENTER)


#페이지 스크롤링 
for a in range(scroll):
    block = d.find_element(By.CSS_SELECTOR, 'div.fysCi')
    d.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', block ) 

#리뷰별로 찾고
data = d.find_elements(By.CSS_SELECTOR, 'div.RHo1pe')

#요소별 추출
def text(x):
    #data = d.find_elements(By.CSS_SELECTOR, 'div.RHo1pe')
    review={}
    review['rat'] = len(x.find_elements(By.CSS_SELECTOR, 'span.Z1Dz7b'))
    review['text'] = x.find_element(By.CSS_SELECTOR, 'div.h3YV2d').text
    review['date'] = x.find_element(By.CSS_SELECTOR, 'span.bp9Aid').text
    return review
    
result=[]
for x in data:
    result.append(text(x))

#result = [text(x) for x in data]

#파일로 저장
df = pd.DataFrame(result)

filename = f'GoogleStoreReview_{app_name}_{len(result)}건_{date_format}.xlsx'
df.to_excel(f_dir+'\\'+filename)
print(f'====== {filename} 파일 생성 완료====== \n======{f_dir}에 저장 완료 ======')