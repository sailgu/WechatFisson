# -*- coding: UTF-8 -*-
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import sys
import time
import re
import argparse

parser = argparse.ArgumentParser(description='set domains in weixin open platform')
parser.add_argument('account_tab', help='open platform account file')
parser.add_argument('--set', help='if set, domain list')
args = parser.parse_args()

def find_by_try(find_method, select_str):
    status = 1
    while(status<5):
        try:
            return find_method(select_str)
        except:
            sleep(0.5*try_time**2)
            status = status + 1
            driver.refresh()
    sys.exit("find \"select_str\" element failed!")

def read_tsv(table, head = True):
    fh = open(table)
    if head:
        head = next(fh)
    return [_.strip().split() for _ in fh]

def exist(find_method, select_str):
    try:
        driver.find_element_by_css_selector(select_str)
    except:
        return False
    return True

#def parser_openid_detail_page():

if args.set:
    domains_to_set = [_.strip() for _ in open(args.set)]

driver = webdriver.Firefox()
wait = WebDriverWait(driver, 5)

driver.get('https://open.weixin.qq.com/')
driver.maximize_window()

language_switch = driver.find_element_by_css_selector('div.menu_placeholder')
ActionChains(driver).move_to_element(language_switch).perform()
time.sleep(0.1)
driver.find_element_by_css_selector('li.menu_list_ele:nth-child(2)').click()
driver.find_element_by_css_selector('#loginBarBt').click()


for account_line in read_tsv(args.account_tab):
    # time.sleep(0.3)
    driver.find_element_by_css_selector('#loginBarBt').click()
    driver.find_element_by_name('account').send_keys(account_line[3])
    driver.find_element_by_name('passwd').send_keys(account_line[4])
    driver.find_element_by_class_name('btn.btn_primary.btn_login').click()

    table = wait.until(EC.presence_of_element_located((By.ID, 'bizplugin_pend')))
    rows = table.find_elements_by_tag_name('tr')[1:]
    for row in rows:
        # switch to one open platform
        detail_button = row.find_element_by_class_name('jsUrlLink')
        detail_button.click()
        driver.switch_to_window(driver.window_handles[1])
        time.sleep(0.5)

        # fectch basic info (appid, gh_id, message_key) to store in table
        open_title = driver.find_element_by_css_selector('.app_name').text
        appid = driver.find_element_by_css_selector('.app_infos > p:nth-child(1)')
        appid = appid.text.split(':')[1]

        ghid = driver.find_element_by_css_selector\
                ('div.wrp_info_item:nth-child(1) > div:nth-child(3) > div:nth-child(2)')
        ghid = ghid.text.split()[0]

        message_key = driver.find_element_by_css_selector\
                ('div.wrp_info_item:nth-child(2) > div:nth-child(3) > div:nth-child(2)')
        message_key = message_key.text

        ### set js share domain
        # enter in modify page
        modify_button = driver.find_element_by_css_selector('.btn_default')
        modify_button.click()
        #time.sleep(0.3)
        if exist(driver.find_elements_by_css_selector, 'span.btn:nth-child(1) > button'):
            driver.find_element_by_css_selector('span.btn:nth-child(1) > button').click()

        # jump to domain set page
        driver.find_element_by_css_selector('#nextBt').click()
        driver.find_element_by_css_selector('#js_next2').click()

        domain_frame = driver.find_element_by_css_selector('#sns_domain_frame')
        # view remain modify times
        remain_times = re.findall(u'本月有(\d)次机会', domain_frame.text)[0]

        # download verify text file
        domain_frame.find_element_by_css_selector('a')

        # get seted domain
        domain_input = domain_frame.find_element_by_css_selector('.frm_input')
        domain_seted = domain_input.get_attribute('value')

        # set domain
        if args.set and len(domains_to_set)>0 and remain_times>0:
            domain_input.send_keys(domains_to_set.pop())
            remain_times = remain_times - 1

            #while(driver.find_element_by_class_name())
            driver.find_element_by_css_selector('#submitBt').click()

        # close current windows and switch to first
        driver.close()
        driver.switch_to_window(driver.window_handles[0])

        # print out detail info
        print '\t'.join(account_line[3:5]+
                [open_title, appid, ghid, message_key, domain_seted, remain_times])

    # finally login out
    driver.find_element_by_css_selector("a.account_meta:nth-child(3)").click()


