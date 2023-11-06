import requests
from bs4 import BeautifulSoup


class codenary_crawl:
    def __init__(self, url):
        self.url = url
        
    def get_company_info(self, url):
        company_res = requests.get(url)
        company_soup = BeautifulSoup(company_res.text, 'html')
        
        parents = company_soup.find('div','mantine-Grid-root mantine-5af20u')
        companies = parents.find_all('div', 'mantine-Grid-col mantine-ne8237')
        
        for company in companies:
        
            com = company.find('div', 'mantine-j3bl35')
            company_location = com.find('div', 'mantine-Text-root mantine-8ytu7x').text
        
            company_detail = requests.get('https://www.codenary.co.kr'+company.a['href'])
            company_detail_soup = BeautifulSoup(company_detail.text, 'html')
        
            company_info = company_detail_soup.find('div', 'mantine-Paper-root mantine-Card-root mantine-jz27g2')
            company_name = company_info.find('div', 'mantine-Text-root mantine-1oj90e9').text
        
            stacks = company_detail_soup.find_all('div', 'mantine-Text-root mantine-7byl33')
        
            for stack in stacks:
                
                self.append([company_name, company_location, stack.text])
            
    def fetch_tech_stack(self, url):

        res = requests.get(url)    
        soup = BeautifulSoup(res.text, "html.parser")
        
        # a 태그 중 필요한 범위 내에서 스택명, 스택 분류 스크래핑하여 리스트에 저장하기
        for a_tag in soup.find_all("a")[7:-2]:
            tech_stack = a_tag.get('id')
            
            # 스택명 별로 상세 페이지에서 스택 분류 스크래핑하기
            detail_page = f"https://www.codenary.co.kr/techstack/detail/{tech_stack}"
            detail_res = requests.get(detail_page)
            detail_soup = BeautifulSoup(detail_res.text, "html.parser")

            tech_type = detail_soup.find("div", class_="mantine-Text-root mantine-7keej3").text
            
            # 리스트에 저장하기
            self.append([tech_type, tech_stack])
