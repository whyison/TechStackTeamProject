from codenary_crawler import codenary_crawl
import pandas as pd

company_info = []
tech_info = []

for i in range(1, 18):
    
    url = 'https://www.codenary.co.kr/company/list?page={}'.format(i)
    codenary_crawl.get_company_info(company_info, url)

for j in range(1, 22):
    
    url = 'https://www.codenary.co.kr/techstack/list?page={}'.format(j)
    codenary_crawl.fetch_tech_stack(tech_info, url)
    
company = pd.DataFrame(company_info)
company.columns = ['회사명', '회사 위치', '스택']

tech = pd.DataFrame(tech_info)
tech.columns = ['직무', '스택']

result = pd.merge(company, tech, left_on = '스택', right_on = '스택', how = 'left')

print(result)