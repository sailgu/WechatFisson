from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import random


IP = '118.190.126.142'
account = 'Kaifangpt013@163.com'
passwd = 'cyhd123456'

driver = webdriver.Firefox()
driver.get('https://open.weixin.qq.com/')
driver.find_element_by_link_text(u'登录').click()
driver.find_element_by_name('account').send_keys(account)
driver.find_element_by_name('password').send_keys(passwd)
driver.find_element_by_class_name('btn btn_primary btn_login').click()
