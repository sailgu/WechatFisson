# -*- coding: UTF-8 -*-
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import sys
import time

def read_tsv(table, head = True):
    fh = open(table)
    res
    if head:
        head = next(fh)
    return [_.strip().split() for _ in fh]



driver = webdriver.Firefox()
wait = WebDriverWait(driver, 5)
driver.get('https://open.weixin.qq.com/')
wait.until(EC.element_to_be_clickable((By.ID, 'loginBarBt'))).click()

for account_line in read_tsv(sys.argv[1]):
    time.sleep(0.5)
    driver.find_element_by_name('account').send_keys(account_line[3])
    driver.find_element_by_name('passwd').send_keys(account_line[4])
    driver.find_element_by_class_name('btn btn_primary btn_login').click()

    table = wait.until(EC.presence_of_element_located((By.ID, 'bizplugin_pend')))
    rows = table.find_elements_by_tag_name('tr')[1:]
    for row in rows:
        open_title = row.find_element_by_class_name('title').text

        row.find_element_by_class_name('jsUrlLink').click()

        driver.switch_to_window(driver.window_handles[1])

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






