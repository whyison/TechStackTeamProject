from wanted_crawler import crawler
from tech_stack_type import tech_stack


def update_stack_type():
    updated_company_info = []
    company_info = crawler()

    for company in company_info:
        for key, value in tech_stack.items():
            if company[-1].lower() in value:
                tech_stack_data = key
                updated_company_info.append([*company, tech_stack_data.title()])
    return updated_company_info
