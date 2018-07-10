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

parser = argparse.ArgumentParser(description='set security domains in weixin offical platform')
parser.add_argument('account_tab', help='offical platform account file')
parser.add_argument('--set', help='if set, domain list')
args = parser.parse_args()

def find_side_button(button_name):
    for ele in driver.find_elements_by_class_name('weui-desktop-menu__name'):
        if ele.text == button_name:
            return ele

def read_tsv(table, head = True):
    fh = open(table)
    if head:
        head = next(fh)
    return [_.strip().split() for _ in fh]

def exist(select_str):
    try:
        driver.find_element_by_css_selector(select_str)
    except:
        return False
    return True

driver = webdriver.Firefox()
wait = WebDriverWait(driver, 5)
driver.get('https://mp.weixin.qq.com/')

fh = open('bussiness_domain_info', 'w')

for account_line in read_tsv(args.account_tab):

    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,
        '[name=account]'))).send_keys(account_line[1])
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,
        '[name=password]'))).send_keys(account_line[2])
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.btn_login'))).click()

    # remind to scan QR code
    print 'pleas scan QR-code to continue'
    while not exist('a.weui-desktop-btn'):
        time.sleep(0.5)

    mp_set_selector = ('ul.weui-desktop-menu:nth-child(1) > li:nth-child(18) >'
        'ul:nth-child(2) > li:nth-child(1) > a:nth-child(1) > span:nth-child(1)'
        ' > span:nth-child(1)')
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, mp_set_selector))).click()

    gh_id_selector = ('div.weui-desktop-setting__box_rows:nth-child(1) > '
        'ul:nth-child(1) > li:nth-child(2) > div:nth-child(2) > '
        'div:nth-child(1) > span:nth-child(1) ')
    gh_id = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, gh_id_selector))).text

    # enter into function setting and fetch bussiness domain
    driver.find_element_by_css_selector('[title=功能设置]').click()
    bussiness_domain = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
        'li.weui-desktop-setting__item:nth-child(3) > div:nth-child(2) > '
        'div:nth-child(1) > strong:nth-child(1)'))).text.replace('\n', ';')

    #if args.set:
    #    driver.find_element_by_css_selector('#jssdkSet').click()

    # enter into auth setting and see if has authed
    driver.find_element_by_css_selector('[title=授权管理]').click()

    # enter into notification panel
    driver.find_element_by_css_selector('.weui-desktop-account__message').click()
    notify_panel = wait.until(EC.presence_of_element_located((By.ID, 'notification')))
    forbids = []
    for notify in driver.find_elements_by_css_selector('.notify_title'):
        if notify.text.count(u'关于违规') < 1:
            continue
        notify.click()
        notify_text = driver.find_element_by_css_selector(
                'dl.notify_item:nth-child(1) > dd:nth-child(2)').text
        forbids = forbids + re.findall(u'(已屏蔽.*?)，', notify_text)
    forbids_str = u';'.join(forbids)

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
    people_set_selector = ('ul.weui-desktop-menu:nth-child(1) > li:nth-child(18) '
        '> ul:nth-child(2) > li:nth-child(2) > a:nth-child(1) > span:nth-child(1) '
        '> span:nth-child(2)')
    driver.find_element_by_css_selector(people_set_selector).click()
    weixin_admin_selector = ('div.frm_control_group:nth-child(3) > '
        'div:nth-child(2) > span:nth-child(1)')
    weixin_admin = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
        weixin_admin_selector))).text

    # print out info
    fh.write(u'\t'.join([weixin_admin] + account_line[1:3] +
            [gh_id, wxid, bussiness_domain, forbids_str]) + "\n")

    # login out
    account_div = driver.find_element_by_css_selector('.weui-desktop-account__info')
    ActionChains(driver).move_to_element(account_div).perform()
    driver.find_element_by_css_selector('li.weui-desktop-dropdown__list-ele:nth-child(5)').click()

fh.close()















