import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import html_module
# import json
import json
# store the URL in url as 
# parameter for urlopen

import logging
import http.client

http.client.HTTPConnection.debuglevel = 1

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True


session = requests.Session()
retry = Retry(total= 2, backoff_factor=0.2, respect_retry_after_header=False)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'
headers = {'User-Agent':user_agent}
url = "https://openx.com/sellers.json"

# store the response of URL
response_from_openx = session.get(url, headers=headers).json()
# storing the JSON response 
# from url in data
# print the json response

def request_sellers(seller, file_name, url=None, counter=0, responseURL=None):
    if counter > 5:
        return
    if not url:
        url = "https://" + seller['domain'] + "/sellers.json"
    try:
        response = session.get(url, headers=headers, timeout=3)
    except Exception as e:
        print(e)
        return
    print('response success')
    if response.status_code == 200:
        if 'application/json' in response.headers.get('Content-Type'):
            raw_res = response.text.encode().decode('utf-8-sig')
            try: 
                response = json.loads(raw_res)
                html_module.generate_row(seller['name'], seller['domain'], seller['seller_type'], len(response['sellers']), '<div class="r_col"><a href="'+ seller['domain'] +'.html">[LINK]</a></div>', file_name)
                branch_counter = counter + 1
                build_branch(response['sellers'], seller['domain'], branch_counter)
                html_module.generate_undersellers_for_link(counter, file_name) 
                print('success in building next branch ' +seller['domain'] )
                html_module.end_row(file_name)
            except Exception:
                html_module.generate_full_row(seller['name'], seller['domain'], seller['seller_type'], '', '<div class="r_col">none</div>', file_name)
        else:
            print('{} - ERROR: it\'s not json. {}'.format(seller['domain'], response.url))
            print(response.headers.get('Content-Type'))
            if  url != response.url and responseURL != response.url:
                if not '/sellers.json' in response.url:
                    url=response.url + '/sellers.json'
                print(url)
                request_sellers(seller, file_name, url, counter, response.url)
            
    else:
        print('{} - ERROR: {}'.format(seller['domain'], response.status_code))
        html_module.generate_full_row(seller['name'], seller['domain'], seller['seller_type'], '', '<div class="r_col">none</div>', file_name)


def build_branch(sellers, file_name, counter=0):
    if not html_module.generate_file(file_name):
        return
    domain_list = []
    for seller in sellers:
        if not seller.get('name'):
            seller['name'] = 'UNAVAILABLE'
        if not seller.get('domain'):
            seller['domain'] = 'UNAVAILABLE'
        if [seller['name'], seller['domain'], seller['seller_type']] in domain_list:
            continue
        domain_list.append([seller['name'], seller['domain'], seller['seller_type']])
        if (seller['seller_type'].upper() == "INTERMEDIARY" or seller['seller_type'].upper() == "BOTH") and not seller['domain'] == 'UNAVAILABLE':
            print(seller['domain']+'\'s requesting sellers...')
            request_sellers(seller, file_name, counter=counter)
        else:
            if not seller['name'] == 'UNAVAILABLE' or not seller['domain'] == 'UNAVAILABLE':
                html_module.generate_full_row(seller['name'], seller['domain'], seller['seller_type'], '', '<div class="r_col">none</div>', file_name)
    html_module.end_file(file_name)


build_branch(response_from_openx['sellers'], 'openx')
