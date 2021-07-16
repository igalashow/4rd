from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import requests
import os
import selenium.common.exceptions
import auth

class Gosuslugi_parser:
    """ """

    def __init__(self):
        pass


    def get_data(self, url):
        """ Получает данные с Госуслуг"""
        driver = webdriver.Chrome()
        driver.get(url)
        timeout = 5
        login = driver.find_element(By.ID, "login")
        passd = driver.find_element(By.ID, "password")
        enter = driver.find_element(By.ID, "loginByPwdButton")

        login.send_keys(auth.login)
        passd.send_keys(auth.passw)
        enter.click()

        cookies = driver.get_cookies()
        source = driver.page_source
        try:
            full_name = driver.find_element_by_xpath(
                "/html/body/my-app/div/div[1]/my-person/div/div/div[2]/my-common-information/div/div/div[2]/div[2]")
            text_full_name = full_name.text
            passport_data = driver.find_element_by_xpath(
                "/html/body/my-app/div/div[1]/my-person/div/div/div[2]/my-common-information/div/div/div[7]/div[2]")
            text_passport_data = passport_data.text
        except selenium.common.exceptions.NoSuchElementException as n:
            print('Паспортные данные отсутствуют', n)
        driver.quit()
        return text_full_name, text_passport_data


    def save_file(self, folder, text, filename='passport_data.txt'):
        """ Сохраняет файл с паспортными данными """

        if not os.path.isfile(folder + '/' + filename):
            os.makedirs(folder)
            with open(folder + '/' + filename, 'w', encoding='utf-8') as f:
                print(text, file=f)
            print(f'Файл с паспортными данными создан по адресу:\n'
                  f'[текущая папка]/{folder}/{filename}')
        else:
            print(f'Файл с паспортными данными уже существует по адресу:\n'
                  f'[текущая папка]/{folder}/{filename}')




gp = Gosuslugi_parser()
data = gp.get_data(url="https://esia.gosuslugi.ru")
gp.save_file(folder=data[0].strip(), text=data[1])


