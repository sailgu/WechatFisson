from selenium import webdriver
import requests
import sys
import time

driver = webdriver.Firefox()
driver.get('http://hd.l23.pw')
(driver.find_element_by_css_selector('.login > li:nth-child(1) > input:nth-child(2)').
        send_keys('xuxiaoming'))
(driver.find_element_by_css_selector('.login > li:nth-child(2) > input:nth-child(2)').
        send_keys('123456'))
driver.find_element_by_css_selector('#doLogin').click()

domain_list, act_id = sys.argv[1:3]

#driver.find_element_by_css_selector('.menu > li:nth-child(7) > a:nth-child(1)').click()
#driver.find_element_by_css_selector('li.now:nth-child(1) > a:nth-child(1)').click()
#driver.find_element_by_css_selector('ul.menu:nth-child(6) > li:nth-child(1) > a:nth-child(1)').click()
driver.get('http://hd.l23.pw/act/domain/%s/' % act_id)

domain_toset = [_.split()[0].strip() for _ in open(domain_list)]
for idx in range(0, len(domain_toset), 2):
    domains = domain_toset[idx:(idx+2)]
    domains_str = '\n'.join(['p.imtt.qq.com']+domains)
    driver.find_element_by_css_selector('#inBtn').click()
    time.sleep(0.2)
    driver.find_element_by_css_selector('#text-domain').send_keys(domains_str)
    driver.find_element_by_css_selector('#appid').send_keys('xasdfasdf')
    driver.find_element_by_css_selector('#oBtnIn').click()
    time.sleep(0.2)




#login_cookies = driver.get_cookies()
#ses_hd = requests.Session()
#for cookies in login_cookies:
#    ses_hd.cookies.set(cookies['name'], cookies['value'])
#
#domain_toset = [_.strip() for _ in open('domain.txt')]
#for idx in range(0, len(domain_toset), 3)
#    postdata = dict(act_id = 134, appid = 'asdaxxx',
#            domain = domain_toset[idx:(idx+3)])
#    ses_hd.post('http://hd.l23.pw/act/add', data = postdata)
