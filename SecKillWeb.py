# -*- coding:utf-8 -*-
'''
@project: SecKillWeb
@file: SecKillWeb.py
@author: kael
@contact: https://github.com/kaelsunkiller
@time: 2020-01-31(星期五) 19:17
@Copyright © 2020. All rights reserved.
'''
import os
import time
import random
import re
from multiprocessing import Process
from utils import create_logger, open_file_os
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys


class SecKillWeb():
    def __init__(self):
        self.logger = create_logger('SecKillWeb')
        self.login_auto = True
        self.users = {}
        self.items_url = []
        self.items_prefer = []
        self.items_num = []
        self.browers = None
        self.check_delay_top = 15
        self.check_delay_btm = 2
        self.always_circle = True
        self.time_out = 24
        self.multi_user = 1
        self.headless = 0
        self.refresh_time = 20
        self.process = []
        self._config()
        self.time_out = self.time_out*3600

    def _config(self):
        config_file = './config.ini'
        if not os.path.exists(config_file):
            self.login_auto = False
            self.logger.warn('config file {} is missing, user needs to login manually.'.format(config_file))
        else:
            with open(config_file, 'r', encoding='utf-8') as configger:
                flag = ''
                info = []
                for line in configger:
                    line = line.strip()
                    line = line.replace('\n', '')
                    if line.startswith('#') or line.startswith(';'):
                        continue
                    if not line:
                        continue
                    if '[user-info]' == line:
                        flag = 'info'
                    elif '[items-url]' == line:
                        flag = 'items'
                    elif '[items-prefer]' == line:
                        flag = 'prefer'
                    elif '[items-num]' == line:
                        flag = 'num'
                    elif '[config-params]' == line:
                        flag = 'params'
                    elif line.startswith('[') and line.endswith(']'):
                        flag = ''
                    elif 'info' == flag:
                        info.append(line)
                    elif 'items' == flag:
                        self.items_url.append(line)
                    elif 'prefer' == flag:
                        if line.isdigit():
                            line = int(line)
                        self.items_prefer.append(line)
                    elif 'num' == flag:
                        if line.isdigit():
                            line = int(line)
                        else:
                            line = 1
                        self.items_num.append(line)
                    elif 'params' == flag:
                        line = line.split('=')
                        if 'check_delay_top' == line[0]:
                            self.check_delay_top = int(line[1])
                        if 'check_delay_btm' == line[0]:
                            self.check_delay_btm = int(line[1])
                        if 'always_circle' == line[0]:
                            self.always_circle = int(line[1])
                        if 'time_out' == line[0]:
                            self.time_out = int(line[1])
                        if 'multi_user' == line[0]:
                            self.multi_user = int(line[1])
                        if 'headless' == line[0]:
                            self.headless = int(line[1])
                for i in range(0, len(info), 2):
                    self.users[info[i]] = info[i+1]
                if not self.users:
                    self.login_auto = False
                    self.logger.warn('[user-info] title is missing, auto login disabled.')
                if not self.items_url:
                    raise Exception('[items-url] title is missing, mission list is empty.')


    def _login_auto(self, browser, user_name, pwd):
        browser.find_element_by_xpath("//*[text()='登录/注册']").click()  # login-btn
        browser.implicitly_wait(5)
        browser.switch_to.frame(browser.find_element_by_xpath("//*[contains(@id,'x-URS-iframe')]"))
        browser.find_element_by_xpath("//*[text()='使用密码验证登录']").click()  # login-use-pwd
        browser.find_element_by_xpath("//*[@id='phoneipt']").send_keys(user_name)  # input-user-name
        click_input = browser.find_element_by_xpath(
            "/html/body/div[2]/div[2]/div[2]/form/div/div[4]/div[2]")  # input-pwd
        ActionChains(browser).move_to_element(click_input).click().send_keys(pwd).perform()
        browser.find_element_by_xpath("//*[@id='submitBtn']").click()  # login
        # while login_btn:
        #     login_btn[0].click()
        #     browser.implicitly_wait(2)
        #     login_btn = browser.find_elements_by_xpath("//*[@id='submitBtn']")

        browser.implicitly_wait(5)  # close pop-up frame
        try:
            WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "j-close-pop-0")))
            browser.find_element_by_class_name("j-close-pop").click()
        except Exception as e:
            self.logger.warn('No pop-up frame detected, please check in 10 sec. If it exits, JUST CLOSE IT.')

    def _login_manual(self, browser):
        self.logger.warn('Please login on this page manually')
        try:
            WebDriverWait(browser, 600).until(EC.presence_of_element_located((By.XPATH, "//*[text()='退出登录']")))
        except Exception as e:
            self.logger.warn('Timeout while waiting for user login manually.')
            browser.quit()
            return False
        return True

    def _check_once(self, browser, prefer=None, num=None, refresh=False):
        buy_btn = browser.find_elements_by_xpath("//*[text()='立即购买']")
        if buy_btn:
            if prefer:
                try:
                    choices = browser.find_element_by_xpath('//*[@class="cont"]').find_elements_by_css_selector('li')
                    if isinstance(prefer, int) and prefer < len(choices):
                        is_active = choices[prefer].find_element_by_css_selector('a').get_attribute('class')
                        if 'dis' not in is_active:
                            choices[prefer].click()
                    elif isinstance(prefer, str):
                        for i, choice in enumerate(choices):
                            text = choice.find_element_by_class_name('title').get_attribute('innerText')
                            if prefer in text:
                                is_active = choice.find_element_by_css_selector('a').get_attribute('class')
                                if 'dis' not in is_active:
                                    choice.click()
                                break
                except Exception as e:
                    self.logger.warn('change prefer error:\n{}'.format(repr(e)))
                    pass
            if num:
                try:
                    in_blank = browser.find_element_by_xpath("//*[@class='u-selnum ']/input")
                    if in_blank.is_enabled():
                        stock = browser.find_elements_by_xpath("//span[@class='stock']")
                        if stock:
                            s_num = re.findall(r'\d+', stock[0].text)
                            if s_num and num > int(s_num[0]):
                                num = int(s_num[0])
                        ActionChains(browser).double_click(in_blank).perform()
                        in_blank.send_keys(num)
                except Exception as e:
                    self.logger.warn('change num error:\n{}'.format(repr(e)))
                    pass
            try:
                buy_btn[0].click()  # buy-now
                browser.find_element_by_xpath("//*[@value='去付款']").click()
                return True
            except Exception as e:
                self.logger.warn('snap up error:{}'.format(repr(e)))
                if not refresh:
                    if self._check_once(browser, prefer=prefer, num=num, refresh=True):
                        return True
                    else:
                        return False
                else:
                    return False
        else:
            return False

    def _browser_activate(self, user_name=None, pwd=None):
        # browser options
        chrome_options = Options()
        prefs = {
            'profile.default_content_setting_values':
                {
                    'notifications': 2
                }
        }
        chrome_options.add_experimental_option('prefs', prefs)
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--log-level=3')
        if self.headless:
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-gpu')
        browser = webdriver.Chrome(options=chrome_options)
        browser.get(self.items_url[0])
        self.logger.warn('starting processing user {} with {} element(s).'.format(user_name, len(self.items_url)))

        try:
            # login once and open urls
            if self.login_auto:
                try:
                    self._login_auto(browser, user_name, pwd)
                except Exception as e:
                    self.logger.warn('{} auto login failed, please check.'.format(user_name))
                    browser.quit()
                    return
            else:
                if not self._login_manual(browser):
                    return
            for url in self.items_url[1:]:
                browser.execute_script("window.open('{}');".format(url))
            windows = browser.window_handles
            self.logger.warn('{} login and open pages success.'.format(user_name))

            # check circles
            i = 0
            time_exc = 0
            while self.always_circle or time_exc < self.time_out:
                current_window = windows[i]
                if current_window != browser.current_window_handle:
                    browser.switch_to.window(current_window)
                item_id = 0
                for r in range(self.refresh_time):
                    browser.refresh()
                    if browser.current_url in self.items_url:
                        item_id = self.items_url.index(browser.current_url) + 1
                        break
                    else:
                        self.logger.debug('user {} refresh time {}, {}'.format(user_name, r, browser.current_url))
                        if r == self.refresh_time-1:
                            self.logger.warn('user {} page {} blocked at {}'.format(user_name, browser.current_window_handle, time_exc))
                if self.items_prefer:
                    prefer = self.items_prefer[item_id-1]
                    if '无' == prefer:
                        prefer = None
                else:
                    prefer = None
                if self.items_num:
                    num = self.items_num[item_id-1]
                    if num < 1:
                        num = None
                else:
                    num = None
                if self._check_once(browser, prefer=prefer, num=num):
                    open_file_os('alarm.wav')
                    if current_window != browser.current_window_handle:
                        browser.switch_to.window(current_window)
                    browser.close()
                    # ActionChains(browser).key_down(Keys.CONTROL).send_keys("w").key_up(Keys.CONTROL).perform()
                    self.logger.warn('{} has mission complete, check now!'.format(user_name))
                    with open('./ALARM.txt', 'a+') as writter:
                        writter.write('{} has mission:\n{}\ncomplete, check now!'.format(user_name, browser.current_url))
                    open_file_os('ALARM.txt')
                    try:
                        windows = browser.window_handles
                        browser.switch_to.window(windows[0])
                        i = 0
                    except Exception as e:
                        self.logger.warn('user:{} mission complete. browser closed.'.format(user_name))
                        break
                else:
                    i += 1
                    if i >= len(windows):
                        i = 0
                        wt = random.randrange(self.check_delay_btm, self.check_delay_top)
                        time.sleep(wt)
                        time_exc += wt
                        self.logger.warn('{} executed time {:.12f}'.format(user_name, time_exc/3600))
            return
        except Exception as e:
            browser.quit()
            raise e

    def multi_user_run(self):
        if not self.login_auto:
            for _ in range(self.multi_user):
                p = Process(target=self._browser_activate)
                self.process.append(p)
        else:
            for key, value in self.users.items():
                p = Process(target=self._browser_activate, args=(key, value))
                self.process.append(p)
        try:
            for p in self.process:
                p.start()
            for p in self.process:
                p.join()
        except Exception as e:
            # for p in self.process:
            #     p.ternimate()
            # os.system("taskkill /f /im chromedriver.exe")
            raise e


if __name__ == '__main__':

    skw = SecKillWeb()
    skw.multi_user_run()