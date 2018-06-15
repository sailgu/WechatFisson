from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains

def isLogined(driver):
    logined_class_name = 'weui-desktop-account__info'
    try:
        driver.find_element_by_class_name(logined_class_name)
    except:
        return False
    else:
        return True

def logout(driver):
    popup = driver.find_element_by_class_name('weui-desktop-account__info')
    ActionChains(driver).move_to_element(popup).perform()
    popups = driver.find_elements_by_class_name('weui-desktop-dropdown__list-ele-contain')
    popups[3].click()

def loginWxOA(account, passwd):
    driver = webdriver.Firefox()
    driver.get('https://mp.weixin.qq.com/')
    if isLogined(driver):
        logout()
    driver.find_element_by_name('account').send_keys(account)
    driver.find_element_by_name('password').send_keys(passwd)
    driver.find_element_by_class_name('btn_login').click()

def setDomin():
    for ele in driver.find_elements_by_class_name('weui-desktop-menu__name'):
        if ele.text == '公众号设置'
            ele.click()
            break
    driver.find_element_by_link_text('功能设置').click()


driver.find_element_by_name('account').send_keys('tlhao06@163.com')
passwd_area = driver.find_element_by_name('password').send_keys('cyhd123456')
driver.find_element_by_class_name('btn_login').click()
