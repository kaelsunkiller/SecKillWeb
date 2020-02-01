from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


user_name = "18155171059"
pwd = "wyyx1059--"
browser = webdriver.Chrome()
windows = browser.window_handles
browser.get('http://you.163.com/item/detail?id=3987138')
# browser.execute_script("window.open('http://you.163.com/item/detail?id=3988740');")
# windows = browser.window_handles
# i = 0
# while windows is not None:
#     window = windows[i]
#     if window != browser.current_window_handle:
#         browser.switch_to.window(window)
#     browser.close()
#     windows = browser.window_handles
#     browser.switch_to.window(windows[0])
#     i = 0
# windows = browser.window_handles

# choices = browser.find_element_by_xpath('//*[@class="cont"]').find_elements_by_css_selector('li')
# for choice in choices:
#     if '没错' in choice.text:
#         choice.click()
# select = choices[3].click()
#
#
# WebDriverWait(browser, 1e10).until(
#     EC.presence_of_element_located((By.XPATH, "//*[text()='退出登录']")))
#
# browser.find_element_by_xpath("//*[text()='登录/注册']").click()    # login-btn
# browser.implicitly_wait(5)
# browser.switch_to.frame(browser.find_element_by_xpath("//*[contains(@id,'x-URS-iframe')]"))
# browser.find_element_by_xpath("//*[text()='使用密码验证登录']").click()    # login-use-pwd
# browser.find_element_by_xpath("//*[@id='phoneipt']").send_keys(user_name)    # input-user-name
# click_input = browser.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/form/div/div[4]/div[2]")   # input-pwd
# ActionChains(browser).move_to_element(click_input).click().send_keys(pwd).perform()
# browser.find_element_by_xpath("//*[@id='submitBtn']").click()   # login
#
# browser.implicitly_wait(5)
# try:
#     WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "j-close-pop-0")))
# except Exception as e:
#     pass
# browser.find_element_by_class_name("j-close-pop").click()

browser.find_element_by_xpath("//*[text()='立即购买']").click()  # buy-now
browser.find_element_by_xpath("//*[@id='confirmRoot']/div/div[3]/div[2]/div[2]/div[2]/div/div[2]/input")

browser.close()