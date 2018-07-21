# -*- coding: UTF-8 -*-
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import os
import time
import re
import argparse
import MySQLdb
import requests as req

parser = argparse.ArgumentParser(description='set security domains in weixin offical platform')
parser.add_argument('account_tab', help='offical platform account file')
parser.add_argument('--set', help='if set, domain list')
args = parser.parse_args()

def check_block(domain):
    domain = domain.split('/')[0]
    domain = re.sub('^(http:|https:)?//', '', domain).split('/')[0]
    if len(domain) < 3:
        return 1
    check_base = "http://check.api-export.com/api/checkdomain"
    playload = {'key': '235e48db60605d00dc64df889dca69e1', 'url': domain}
    try:
        check_response = req.get(check_base, params = playload)
        return json.loads(check_response.text)['code']
    except:
        return '.'

def find_side_button(button_name):
    for ele in driver.find_elements_by_class_name('weui-desktop-menu__name'):
        if ele.text == button_name:
            return ele

def read_tsv(table, head = True):
    fh = open(table)
    if head:
        head = next(fh)
    res = [_.strip().split() for _ in fh]
    fh.close()
    return res

def exist(select_str):
    try:
        driver.find_element_by_css_selector(select_str)
    except:
        return False
    return True

def get_viewed():
    if os.path.exists('offical_platform.domain.tab'):
        return set([_[0]for _ in read_tsv('offical_platform.domain.tab')])
    else:
        return set()


viewed_account = get_viewed()
if args.set:
    viewed_account = set()
    domains_to_set = [_.strip() for _ in open(args.set)]
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




driver = webdriver.Firefox()
wait = WebDriverWait(driver, 10)
driver.get('https://mp.weixin.qq.com/')

fh = open('offical_platform.domain.set_af.tab', 'a', 0)
fh.write('account\tpasswd\tadmin\tgh_id\twx_id\tdomains\tstatus\n')

for account_line in read_tsv(args.account_tab):
    if account_line[0] in viewed_account:
        continue

    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,
        '[name=account]'))).send_keys(account_line[0])
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,
        '[name=password]'))).send_keys(account_line[1])
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.btn_login'))).click()

    # get admin account
    weixin_admin = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
        '.status > p:nth-child(2)')))
    weixin_admin = re.findall(u'\((.*?)\)', weixin_admin.text)[0]
    #print u'\t'.join(account_line + [weixin_admin])
    #driver.back()
    #continue

    # remind to scan QR code
    print 'pleas scan QR-code to continue'
    while not exist('a.weui-desktop-btn'):
        #wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.weui-desktop-btn')))
        time.sleep(0.5)

    # offical account setting
    mp_set_selector = ('ul.weui-desktop-menu:nth-child(1) > li:nth-child(18) >'
        'ul:nth-child(2) > li:nth-child(1) > a:nth-child(1) > span:nth-child(1)'
        ' > span:nth-child(1)')
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, mp_set_selector))).click()

    gh_id_selector = ('div.weui-desktop-setting__box_rows:nth-child(1) > '
        'ul:nth-child(1) > li:nth-child(2) > div:nth-child(2) > '
        'div:nth-child(1) > span:nth-child(1) ')
    gh_id = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, gh_id_selector))).text

    ## enter into function setting and fetch bussiness domain
    driver.find_element_by_css_selector('[title=功能设置]').click()
    bussiness_domain = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
        'li.weui-desktop-setting__item:nth-child(3) > div:nth-child(2) > '
        'div:nth-child(1) > strong:nth-child(1)'))).text.replace('\n', ';')

    driver.find_element_by_id('trustedDomain').click()
    remain_times = driver.find_element_by_css_selector('div.group:nth-child(1) > '
            'p:nth-child(6) > span:nth-child(1)').text
    domains_form = driver.find_element_by_css_selector('.frm_domain')
    domain_inputs = [domains_form.find_element_by_css_selector('.js_domain' + str(_)) for _ in range(1,4)]
    domain_good_count = map(lambda x: check_block(x.get_attribute('value')), domain_inputs).count(0)
    if int(remain_times)>0 and args.set and domain_good_count < 1:
        bussiness_domain = ''
        for domain_input in domain_inputs:
            domain_text = domain_input.get_attribute('value')
            if len(domains_to_set)>0 and (len(domain_text)<3 or check_block(domain_text)):
                domain_input.clear()
                domain_input.send_keys(domains_to_set.pop(0))
            bussiness_domain = bussiness_domain + ';' + domain_input.get_attribute('value')
        while exist('span.btn:nth-child(1) > button:nth-child(1)'):
            driver.find_element_by_css_selector('span.btn:nth-child(1) > button:nth-child(1)').click()
    else:
        driver.find_element_by_css_selector('span.btn:nth-child(2) > button:nth-child(1)').click()
    bussiness_domain.strip(';')


    #if args.set:
    #    driver.find_element_by_css_selector('#jssdkSet').click()

    ## enter into auth setting and see if has authed
    driver.find_element_by_css_selector('[title=授权管理]').click()
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'th.table_cell:nth-child(1)')))
    auth_paltforms = '.'
    if not exist('.empty_tips'):
        auth_table = driver.find_element_by_id('js_body')
        auth_h4s = auth_table.find_elements_by_tag_name('h4')
        auth_paltforms = ';'.join([_.text for _ in auth_h4s])

    # enter into notification panel
    driver.find_element_by_css_selector('.weui-desktop-account__message').click()
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.notify_title')))
    forbids = []
    for notify in driver.find_elements_by_css_selector('.notify_title'):
        if notify.text.count(u'关于违规') < 1:
            continue
        notify.click()
        notify_text = (notify.find_element_by_xpath('../../..').
                find_element_by_css_selector('dd').get_attribute('innerHTML'))
        forbids = forbids + re.findall(u'(已屏蔽.*?)，', notify_text)
    forbids_str = u';'.join(set(forbids))

    # enter into basic setting page
    basic_set_selector = ('ul.weui-desktop-menu:nth-child(1) > li:nth-child(20) '
        '> ul:nth-child(2) > li:nth-child(1) > a:nth-child(1) > span:nth-child(1) '
        '> span:nth-child(1)')
    driver.find_element_by_css_selector(basic_set_selector).click()
    wxid_selector = ('div.section:nth-child(1) > div:nth-child(2) > '
        'div:nth-child(1) > div:nth-child(2) > p:nth-child(1)')
    wxid = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
        wxid_selector))).text

    # weixin account binding to this offical account
    #people_set_selector = ('ul.weui-desktop-menu:nth-child(1) > li:nth-child(18) '
    #    '> ul:nth-child(2) > li:nth-child(2) > a:nth-child(1) > span:nth-child(1) '
    #    '> span:nth-child(2)')
    #driver.find_element_by_css_selector(people_set_selector).click()
    #weixin_admin_selector = ('div.frm_control_group:nth-child(3) > '
    #    'div:nth-child(2) > span:nth-child(1)')
    #weixin_admin = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
    #    weixin_admin_selector))).text

    # print out info
    fh.write((u'\t'.join(account_line[0:2] + [weixin_admin, gh_id, wxid,
        bussiness_domain, str(remain_times), auth_paltforms, forbids_str]) + u"\n").encode('utf-8'))

    # login out
    account_div = driver.find_element_by_css_selector('.weui-desktop-account__info')
    ActionChains(driver).move_to_element(account_div).perform()
    driver.find_element_by_css_selector('li.weui-desktop-dropdown__list-ele:nth-child(5)').click()

fh.close()


