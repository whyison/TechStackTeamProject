from selenium import webdriver
from selenium.webdriver import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def repeat_scroll(driver):
    scroll_location = driver.execute_script("return document.body.scrollHeight")

    while True:
        
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

        time.sleep(2)

        scroll_height = driver.execute_script("return document.body.scrollHeight")

        if scroll_location == scroll_height:
            break
        
        else:
            scroll_location = driver.execute_script("return document.body.scrollHeight")
            

jobs = {'하드웨어 엔지니어' : 672, '빅데이터 엔지니어' : 1025, '보안 엔지니어' : 671, '프로덕트 매니저' : 876, '크로스플랫폼 앱 개발자' : 10111, 'DBA' : 10231, '블록체인 플랫폼 엔지니어' : 1027,
       'ERP전문가' : 10230, 'PHP 개발자' : 893, '영상,음성 엔지니어' : 896, '.NET 개발자' : 661, '웹 퍼블리셔' : 939, 
       'CTO,Chief Technology Officer' : 795, '그래픽스 엔지니어' : 898, 'BI 엔지니어' : 1022, 'VR 엔지니어': 10112, 
       '루비온레일즈 개발자' : 894, 'CIO,Chief Information Officer' : 793}

for job in jobs:
    url = 'https://www.wanted.co.kr/wdlist/518/{}?country=kr&job_sort=job.latest_order&years=0&locations=all'.format(jobs[job])
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)
    
    repeat_scroll(driver)
    
    company_links = []
    
    companies = list(driver.find_elements(By.CLASS_NAME, 'Card_className__u5rsb'))

    for company in companies:
        company_links.append(driver.execute_script("return arguments[0].getAttribute('href');", company.find_element(By.TAG_NAME, 'a')))

    
    
    for link in company_links:
        url = 'https://www.wanted.co.kr'+link
        
        driver.get(url)
        time.sleep(2)
        
        elem = driver.find_element(By.XPATH, '//*[@id="__next"]/div[3]/div[1]/div[1]/div/div[2]/hr')
        height = driver.execute_script("return arguments[0].getBoundingClientRect().top;", elem)
        
        driver.execute_script(f"window.scrollTo(0, {height});")

        time.sleep(2)
        
        tech_stacks = driver.find_elements(By.CLASS_NAME, 'JobDescription_JobDescription_skill_wrapper__9EdFE')
        company_name = driver.title.split(' ')[0][1:-1]
        company_location = driver.find_element(By.XPATH, '//*[@id="__next"]/div[3]/div[1]/div[1]/div/div[2]/section[2]/div[2]/span[2]')
        print(company_location.text)
        tech = ''
        for tech_stack in tech_stacks:
            tech += tech_stack.text
            
        tech = tech.split('\n')
            
        
        
