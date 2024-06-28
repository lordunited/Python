import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re
import HtmlTestRunner
import requests
from selenium.webdriver.support.wait import WebDriverWait
import getpass
headers = {
    'authority': '#your_domain',
    "cookie": "",
    "origin": "#your_domain",
    "referer": "",
    "x-requested-with": "XMLHttpRequest",
}

response = requests.post('https://#your_domain/Shop/GenerateContractNo', headers=headers)
reponse_co = str(response.content)
reponse_co_num = re.findall('[0-9]+', reponse_co)
class appImport(unittest.TestCase):

    def setUp(self):
        options = Options()
        options.add_argument("--headless")  # Runs Chrome in headless mode.
        # options.add_argument('--no-sandbox')  # Bypass OS security model
        # options.add_argument('--disable-gpu')  # applicable to windows os only
        options.add_argument('start-maximized')  #
        options.add_argument('disable-infobars')
        options.add_argument("--disable-extensions")
        #self.driver = webdriver.Chrome(executable_path=r'C:\chromedriver.exe')
        self.driver = webdriver.Chrome(chrome_options=options,executable_path=r'c:\chromedriver.exe')
        # driver.get("http://google.com/")
        print("Headless Chrome Initialized on Windows OS")
        # driver = webdriver.Chrome(executable_path=r'c:\chromedriver.exe', chrome_options=options)
        # self.chrome_options = Options()
        # self.chrome_options.add_argument('--headless')
        # self.chrome_options = self.Options()
        # self.chrome_options.add_argument('--headless')
        # self.chrome_options.add_argument('--disable-gpu')
        self.driver.maximize_window()
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.google.com/"
        self.verificationErrors = []
        self.accept_next_alert = True
    def shenase_id(self):
        requests.post()
    def login_(self):
        driver = self.driver
        driver.get("https://#your_domain")
        driver.find_element_by_id("UserName").clear()
        # driver.find_element_by_id("UserName").send_keys("testbrocker")
        driver.find_element_by_id("UserName").send_keys("usertest")
        driver.find_element_by_id("Password").clear()
        # driver.find_element_by_id("Password").send_keys("testbrocker1234")
        driver.find_element_by_id("Password").send_keys("usertest1234")
        driver.find_element_by_id("m_login_signin_submit").click()
    def test__import(self):
        driver = self.driver
        driver.get("https://#your_domain")
        driver.find_element_by_id("UserName").clear()
        #driver.find_element_by_id("UserName").send_keys("testbrocker")
        driver.find_element_by_id("UserName").send_keys("usertest")
        driver.find_element_by_id("Password").clear()
        #driver.find_element_by_id("Password").send_keys("testbrocker1234")
        driver.find_element_by_id("Password").send_keys("usertest1234")
        driver.find_element_by_id("m_login_signin_submit").click()
        driver.get("https://#your_domain/")
        driver.get("https://#your_domain/Shop/Create")
        driver.find_element_by_id("EnName").click()
        driver.find_element_by_id("EnName").clear()
        driver.find_element_by_id("EnName").send_keys("ZamanianDamavand")
        driver.find_element_by_id("OwnerName").click()
        driver.find_element_by_id("OwnerName").click()
        driver.find_element_by_id("OwnerName").clear()
        driver.find_element_by_id("select2-BusinessTypeId-container").click()
        driver.find_element_by_xpath("//span/span/input").click()
        driver.find_element_by_xpath("//span/span/input").clear()
        # driver.find_element_by_xpath("//span/span/input").send_keys(u"خدمات برنامه نویسی کامپیوتر ، طراحی")
        driver.find_element_by_xpath("//span/span/input").send_keys(Keys.ENTER)
        # time.sleep(5)
        # driver.find_element_by_id("FaName").click()
        # driver.find_element_by_id("FaName").clear()
        driver.find_element_by_id("OwnerLastName").click()
        driver.find_element_by_id("OwnerLastName").clear()
        driver.find_element_by_id("SubBusinessTypeId").click()
        driver.find_element_by_id("PropertyTypeId").click()
        #driver.find_element_by_id("GroupId").click()
        driver.find_element_by_id("ProjectTypeId").click()
        driver.find_element_by_id("ProjectTypeId").click()
        driver.find_element_by_id("ProjectTypeId").click()
        driver.find_element_by_id("ProjectTypeId").click()
        driver.find_element_by_id("ContractNo").send_keys(reponse_co_num[0])
        print(reponse_co_num[0])
        driver.find_element_by_xpath("//a[@id='Checking']/span").click()
        time.sleep(5)
        driver.find_element_by_xpath(u"(.//*[normalize-space(text()) and normalize-space(.)='×'])[3]/following::button[1]").click()
        driver.find_element_by_id("FatherNameSignatory").clear()
        driver.find_element_by_id("FatherNameSignatory").send_keys(u"عباس")
        driver.find_element_by_id("EnNameSignatory").click()
        driver.find_element_by_id("EnNameSignatory").clear()
        driver.find_element_by_id("EnFatherNameSignatory").click()
        driver.find_element_by_id("EnFatherNameSignatory").clear()
        driver.find_element_by_id("EnFatherNameSignatory").send_keys("abas")
        driver.find_element_by_id("CustomerType").click()
        driver.find_element_by_id("Gender").click()
        Select(driver.find_element_by_id("Gender")).select_by_visible_text(u"آقا")
        driver.find_element_by_id("IdNumber").send_keys("2222")
        driver.find_element_by_id("IdentifierSerial").click()
        driver.find_element_by_id("IdentifierSerial").clear()
        driver.find_element_by_id("IdentifierSerial").send_keys("73962")
        driver.find_element_by_id("LetterIdentifierSeries").click()
        driver.find_element_by_id("NumberIdentifierSeries").click()
        driver.find_element_by_id("NumberIdentifierSeries").clear()
        driver.find_element_by_id("NumberIdentifierSeries").send_keys("20")
        time.sleep(7)
        driver.find_element_by_xpath("//button[@id='next']/span/span").click()
        time.sleep(5)
        driver.find_element_by_id("AreaId").click()
        Select(driver.find_element_by_id("AreaId")).select_by_visible_text("1")
        driver.find_element_by_id("postalCode").click()
        driver.find_element_by_id("postalCode").send_keys("14676000000")
        driver.find_element_by_id("ShortAddress").click()
        driver.find_element_by_id("ShortAddress").clear()
        driver.find_element_by_id("FullAddress").click()
        driver.find_element_by_id("FullAddress").clear()
        driver.find_element_by_id("EnFullAddress").click()
        driver.find_element_by_id("EnFullAddress").clear()
        driver.find_element_by_id("EnFullAddress").send_keys("tehran")
        driver.find_element_by_id("FirstReagentFullName").click()
        driver.find_element_by_id("FirstReagentFullName").clear()
        driver.find_element_by_id("FirstReagentPhoneNo").click()
        driver.find_element_by_xpath("//button[@id='next']/span/span").click()
        time.sleep(5)
        time.sleep(3)
        #driver.find_element_by_id("#fupCDFFFile").send_keys(os.getcwd() + "C:/fakepath/testapp.jpg")
        # upload_file = driver.find_element_by_id("fupCDFFFile")
        time.sleep(25)
        driver.find_element_by_xpath("//button[@id='next']/span/span").click()
        time.sleep(20)
        time.sleep(5)
if __name__ == '__main__':
    unittest.main(
        testRunner=HtmlTestRunner.HTMLTestRunner(output='C:/Users/mohammadreza/PycharmProjects/pythonProject/reports'))
    print("test run and its ok")
