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

parser = argparse.ArgumentParser(
        description='delet blocked domain and create new domain in Pubyun.com')
parser.add_argument('account', help='account for Pubyun.com')
parser.add_argument('password', help='password for Pubyun.com')
parser.add_argument('--ip', default = '118.190.126.142', help='ip for the domain')
parser.add_argument('--number', type = int,  default = 12,
        help='number of domain to create')
args = parser.parse_args()

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
    print row.get_attribute('innerHTML')
    if domain_str in need_removed and domain == domain_str:
        cell[5].find_element_by_class_name('delete').click()
        print domain_str, "find in bad domain list, so will be deleted"
        raw_input("Press Enter to delet it and continue...")
        wait.until(EC.element_to_be_clickable((By.ID, 'rrdelete_button'))).click()

fh = open('domain.txt', 'w')
for idx in range(args.number):
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, u'创建动态域名'))).click()
    uncreated_domains = []
    while len(uncreated_domains) < 1:
        domin_input = driver.find_element_by_id('dyndns_name')
        domin_input.clear()
        domin_input.send_keys(str(domain_idx_max+idx+1)+random_generator(12))
        driver.find_element_by_partial_link_text(".8800.org").click()
        #driver.find_element_by_partial_link_text(".8800.org").click()
        driver.find_element_by_id('form_win_button').click()

        table = wait.until(EC.presence_of_element_located((By.ID, 'dyndns_table')))
        rows = table.find_elements_by_tag_name('tr')[1:]
        for row in rows:
            cell = row.find_elements_by_tag_name('td')
            if cell[0].text.count(u'已被创建') == 0 :
                domain_extract = cell[0].text.split()[0]
                if domain_extract.count('.3322.') or domain_extract.count('.8800.'):
                    uncreated_domains.append([cell[0].text.split()[0], row])

    choiced_domain = random.choice(uncreated_domains)
    raw_input(choiced_domain[0]+' will created, Press Enter to continue...')
    choiced_domain[1].find_element_by_link_text(u'创建域名').click()
    time.sleep(3)
    if driver.find_element_by_id('rr_result').text.count(u'个数已满')>0:
        print u'创建的域名个数已满，需要创建更多动态域名，请购买二级域名'
        exit()
    fh.write(choiced_domain[0]+'\n')
    ip_set = (driver.find_element_by_partial_link_text(choiced_domain[0]).
               find_element_by_xpath('../..'))
    #print ip_set.get_attribute('innerHTML')
    ip_set.find_element_by_class_name('editor').click()
    ip_set = wait.until(EC.presence_of_element_located((By.NAME, 'ip')))
    ip_set.clear()
    ip_set.send_keys(IP)
    driver.find_element_by_id('rr_postbtn').click()


