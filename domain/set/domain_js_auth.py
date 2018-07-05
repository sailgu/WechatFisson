# -*- coding: UTF-8 -*-
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import sys
import time



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
    res
    if head:
        head = next(fh)
    return [_.strip().split() for _ in fh]

def parser_openid_detail_page():



driver = webdriver.Firefox()
wait = WebDriverWait(driver, 5)

driver.get('https://open.weixin.qq.com/')
driver.maximize_window()

language_switch = driver.find_element_by_css_selector('div.menu_placeholder')
ActionChains(driver).move_to_element(language_switch).perform()
driver.find_element_by_css_selector('li.menu_list_ele:nth-child(2)').click()
driver.find_element_by_css_selector('#loginBarBt').click()


for account_line in read_tsv(sys.argv[1]):
    time.sleep(0.5)
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

        # fectch basic info (appid, gh_id, message_key) to store in table
        open_title = driver.find_element_by_css_selector('.app_name')
        appid = driver.find_element_by_css_selector('.app_infos > p:nth-child(1)')
        appid = appid.text.split(':')[1]

        ghid = driver.find_element_by_css_selector\
                ('div.wrp_info_item:nth-child(1) > div:nth-child(3) > div:nth-child(2)')
        ghid = ghid.text.split()[0]

        message_key = driver.find_element_by_css_selector\
                ('div.wrp_info_item:nth-child(2) > div:nth-child(3) > div:nth-child(2)')
        message_key = message_key.text

        ### set js share domain
        # jump to domain set page
        modify_button = driver.find_element_by_css_selector('.btn_default')
        modify_button.click()
        driver.find_element_by_css_selector('#nextBt').click()
        driver.find_element_by_css_selector('#js_next2').click()

        domain_frame = driver.find_element_by_css_selector('#sns_domain_frame')
        # view remain modify times
        remain_times = re.findall(u'本月有(\d)次机会', domain_frame.text)[0]

        # download verify text file
        domain_frame.find_element_by_css_selector('a')

        # set domain
        if set_domain:
            domain_input = domain_frame.find_element_by_css_selector('.frm_input')
            domain_input.send_keys()
            remain_times = remain_times - 1

        #finally submit and login out
        driver.find_element_by_css_selector('#submitBt').click()









        wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, 'a.btn.btn_default.js_promp'))).click()

        try:
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.js_btn'))).click()
        except:
            pass
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a#nextBt.btn.btn'))).click()
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a#js_next2'))).click()
        mp_input = wait.until(EC.presence_of_element_located((By.NAME, 'white_mp')))
        mp_input.clear()
        mp_input.send_keys('')
        domain_input = driver.find_element_by_css_selector('input[name=sns_domain]')
        domain_input.clear()
        domain_input.send_keys('')
        submit = driver.find_element_by_css_selector('a#submitBt.btn.btn_primary.jsSendBt')
        while driver.find_element_by_css_selector('a#submitBt.btn.btn_primary.jsSendBt'):
            submit.click
            time.sleep(0.5)






