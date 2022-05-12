import json

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

import html_module

files_made = []
files_failed = []

def build(to_build):
    new_branches = []
    for branch in to_build:
        if branch[0] in files_made or branch[0] in files_failed:
            pass
        else:
            new_branches.append(build_branch(domain =  branch[0], birth_path = branch[1], new_branches = new_branches))
    build(new_branches)

def build_branch(domain, birth_path, new_branches):
    sellers = request_sellers(domain)
    if sellers:
        already_built = []
        html_module.generate_file(domain)
        for seller in sellers:
            sellers_data = check_if_seller_has_data(seller)
            sellers_name = sellers_data[1][0]
            sellers_domain = sellers_data[1][1]
            sellers_type = sellers_data[1][2]
            if [sellers_name, sellers_domain, sellers_type] in already_built:
                continue
            if sellers_data[0]:
                already_made = False
                for row in files_made:
                    if sellers_domain in row:
                        already_made = True
                        html_module.build_row(domain, sellers_name, sellers_domain, sellers_type, 'built')
                        already_built.append([sellers_name, sellers_domain, sellers_type])
                        break
                if already_made:
                    break
                else:
                    if sellers_domain in birth_path:
                        html_module.build_row(domain, sellers_name, sellers_domain, sellers_type, 'child')
                        already_built.append([sellers_name, sellers_domain, sellers_type])
                    else:
                        html_module.build_row(domain, sellers_name, sellers_domain, sellers_type, 'building')
                        new_path = birth_path.copy()
                        new_path.append(sellers_domain)
                        new_branches.append([sellers_domain, new_path])
                        already_built.append([sellers_name, sellers_domain, sellers_type])
            else:
                html_module.build_row(domain, sellers_name, sellers_domain, sellers_type, 'none')
                already_built.append([sellers_name, sellers_domain, sellers_type])
        html_module.end_file(domain)
        file_made = True
    else:
        file_made = False
    edit_masters(file_made, birth_path)
    return new_branches

def check_if_seller_has_data(seller):
    name = seller.get('name')
    domain = seller.get('domain')
    seller_type = seller.get('seller_type')
    if not name:
        name = 'UNAVAILABLE'
    if not domain:
        domain = 'UNAVAILABLE'        
    if not seller_type:
        seller_type = 'UNAVAILABLE'
    if (seller_type =='BOTH' or seller_type == 'INTERMEDIARY') and domain != 'UNAVAILABLE':
        return (True, [name, domain, seller_type])
    else:
        return (False, [name, domain, seller_type])

def edit_masters(file_made, birth_path):
    if len(birth_path) < 2:
        return
    if file_made:
        html_module.edit_row(birth_path[-1], birth_path, 'LINK')
        for master in birth_path:
            html_module.edit_depth(birth_path, master)
        files_made.append(birth_path[-1])
    else:
        html_module.edit_row(birth_path[-1], birth_path, 'failed')
        files_failed.append(birth_path[-1])

def request_sellers(domain, url=None, responseURL=None):
    if not url:
        url = "https://" + domain + "/sellers.json"
    print(url+'\'s requesting sellers...')
    try:
        response = session.get(url, headers=headers, timeout=3)
    except Exception as error:
        print('ERROR: Could not get the response from: {}. {}'.format(domain, error))
        return None
    print('Response success - {}'.format(url))
    if response.status_code == 200:
        content_type = response.headers.get('Content-Type')
        if not content_type:
            content_type = ''
        if 'application/json' in content_type:
            raw_res = response.text.encode().decode('utf-8-sig')
            try: 
                response = json.loads(raw_res)
                return response['sellers']
            except Exception:
                print(url + 'JSON decoding failure.')
                return None
        else:
            print('{} - ERROR: It\'s not json. Retrieved redirect url: {}'.format(domain, response.url))
            if  url != response.url and responseURL != response.url:
                if not '/sellers.json' in response.url:
                    url=response.url + '/sellers.json'
                print(url)
                return request_sellers(domain, url, response.url)
            else:
                print('Redirect failed')
                return None
    else:
        print('{} - ERROR: {}'.format(domain, response.status_code))
        return None

session = requests.Session()
retry = Retry(total= 2, backoff_factor=0.2, respect_retry_after_header=False)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'
headers = {'User-Agent':user_agent}

to_build = [['openx.com', ['openx.com']]]
build(to_build)
