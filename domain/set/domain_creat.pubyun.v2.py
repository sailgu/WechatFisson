# -*- coding: UTF-8 -*-
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import random
import string
import MySQLdb
import re
import argparse
import requests

parser = argparse.ArgumentParser(
        description='delet blocked domain and create new domain in Pubyun.com')
parser.add_argument('account', help='account for Pubyun.com')
parser.add_argument('password', help='password for Pubyun.com')
parser.add_argument('--ip', default = '118.190.126.142', help='ip for the domain')
parser.add_argument('--number', type = int,  default = 12,
        help='number of domain to create')
args = parser.parse_args()

def check_block(domain):
    domain = domain.split('/')[0]
    domain = re.sub('^(http:|https:)?//', '', domain).split('/')[0]
    check_base = "http://check.api-export.com/api/checkdomain"
    playload = {'key': '235e48db60605d00dc64df889dca69e1', 'url': domain}
    try:
        check_response = requests.get(check_base, params = playload)
        return json.loads(check_response.text)['code']
    except:
        return '.'

def random_generator(size=6, chars=string.ascii_lowercase):
    return ''.join(random.choice(chars) for x in range(size))

IP = args.ip
account = args.account
passwd = args.password

driver = webdriver.Firefox()
wait = WebDriverWait(driver, 10)

driver.get('http://www.pubyun.com/accounts/signin/')
driver.find_element_by_id('id_identification').send_keys(account)
driver.find_element_by_id('id_password').send_keys(passwd)
driver.find_element_by_class_name('btn_login').click()

wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'left_navtit'))).click()
wait.until(EC.element_to_be_clickable((By.LINK_TEXT, '域名列表'))).click()

login_cookies = driver.get_cookies()
csrftoken = driver.get_cookie('csrftoken')['value']
ses_pub = requests.Session()
for cookies in login_cookies:
    ses_pub.cookies.set(cookies['name'], cookies['value'])

table = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'gy_result_tb')))
rows = table.find_elements_by_tag_name('tr')[1:]

conn = MySQLdb.connect(host='47.104.154.233', user='juyh', passwd='u3y4f2',
        db='huodong', port=3306)
sql_domain = "select domain from domain where status=1"
cur = conn.cursor()
cur.execute(sql_domain)
bad_domain = set([_[0].strip() for _ in cur.fetchall()])

sql_domain1 = "select domain from domain1 where status=1"
cur = conn.cursor()
cur.execute(sql_domain1)
bad_domain = bad_domain | set([_[0].strip() for _ in cur.fetchall()])


all_domain = "select domain from domain"
cur = conn.cursor()
cur.execute(all_domain)
all_domains = set([_[0].strip() for _ in cur.fetchall()])


all_domain1 = "select domain from domain1"
cur = conn.cursor()
cur.execute(all_domain1)
all_domains = all_domains | set([_[0].strip() for _ in cur.fetchall()])

created_domain = set([_.find_elements_by_tag_name('td')[1].text.strip() for _ in rows])
matched_number = [re.findall('^\d+', _) for _ in created_domain]
domain_idx_max = max([int(_[0]) for _ in matched_number if len(_)>0] + [0])

noexist_domain = set([ _ for _ in created_domain if _ not in all_domains])

need_removed = created_domain - (created_domain - bad_domain)
need_removed = noexist_domain | need_removed

for domain in need_removed:
    row = (driver.find_element_by_partial_link_text(domain).
            find_element_by_xpath('../..'))
    cell = row.find_elements_by_tag_name('td')
    domain_str = cell[1].text.strip()
    #print row.get_attribute('innerHTML')
    if domain_str in need_removed and domain == domain_str:
        print domain_str, "find in bad domain list, so will be deleted"
        raw_input("Press Enter to delet it and continue...")
        ses_pub.get('http://www.pubyun.com/user/dyndns/rrs/' +
            cell[4].find_element_by_tag_name('a').get_attribute('rel') + '/remove/')

fh = open('domain.txt', 'a')
for idx in range(args.number):
    domain_name = str(domain_idx_max+idx+1) + random_generator(12)
    formdata = dict(csrfmiddlewaretoken = csrftoken, name = domain_name,
            ip = args.ip, domainid='8866.org')
    raw_input(domain_name +'.8866.org will created, Press Enter to continue...')
    ses_pub.post('http://www.pubyun.com/user/dyndns/rrs/addrrs/2/', data = formdata)
    fh.write(domain_name+'.8866.org\n')


