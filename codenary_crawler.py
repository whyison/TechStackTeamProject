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
            
    def get_tech_info(self, url):
        stack_res = requests.get(url)
        stack_soup = BeautifulSoup(stack_res.text, 'html')
        
        parents = stack_soup.find('div','mantine-Grid-root mantine-5af20u')
        dev_stacks = parents.find_all('div', 'mantine-Grid-col mantine-ne8237')
        
        for dev_stack in dev_stacks:
        
            dev = dev_stack.find('div', 'mantine-j3bl35')
            stack_name  = dev.find('div', 'mantine-Text-root mantine-xn0h5k').text
            stack_class  = dev.find('div', 'mantine-Text-root mantine-8ytu7x').text
        
            self.append([stack_name, stack_class])
