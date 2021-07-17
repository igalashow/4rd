from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import os
import selenium.common.exceptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import auth


class Gosuslugi:
    """ """

    def __init__(self):
        pass


    def login_to_gosuslugi(self, url, log_in, passw):
        """ Логин в портал Госуслуг """
        try:
            #### для запуска браузера "без головы" (Линукс, под Win7HB не работает)
            # op = webdriver.ChromeOptions()
            # op.add_argument('--disable-gpu')
            # op.add_argument('--disable-extensions')
            # op.add_argument('--headless')
            # driver = webdriver.Chrome(options=op)

            driver = webdriver.Chrome()
            driver.get(url)
            element_present = EC.presence_of_element_located((By.ID, 'login'))
            WebDriverWait(driver, timeout=15).until(element_present)

            login = driver.find_element(By.ID, "login")
            passd = driver.find_element(By.ID, "password")
            enter = driver.find_element(By.ID, "loginByPwdButton")

            login.send_keys(log_in)
            passd.send_keys(passw)
            enter.click()


        except selenium.common.exceptions.TimeoutException as n:
            print('Таймаут подключения', n)
            quit()
        except Exception as e:
            print('Что-то пошло не так. Выход.', e)
            quit()
        return driver


    def get_data(self, driver):
        """ Получает паспортные данные с Госуслуг"""
        try:
            element_present = EC.presence_of_element_located((By.XPATH,
                '/html/body/my-app/div/div[1]/my-person/div/div/div[2]/my-common-information/div/div/div[2]/div[2]'))
            WebDriverWait(driver, timeout=10).until(element_present)

            full_name = driver.find_element_by_xpath(
                "/html/body/my-app/div/div[1]/my-person/div/div/div[2]/my-common-information/div/div/div[2]/div[2]")
            text_full_name = full_name.text
            passport_data = driver.find_element_by_xpath(
                "/html/body/my-app/div/div[1]/my-person/div/div/div[2]/my-common-information/div/div/div[7]/div[2]")
            text_passport_data = passport_data.text
        except selenium.common.exceptions.NoSuchElementException as n:
            print('Паспортные данные отсутствуют', n)
            quit()
        except selenium.common.exceptions.TimeoutException as n:
            print('Таймаут подключения', n)
            quit()
        except Exception:
            print('Что-то пошло не так. Выход.')
            quit()
        # driver.quit()
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




g = Gosuslugi()
data = g.get_data(g.login_to_gosuslugi(url="https://esia.gosuslugi.ru", log_in=auth.login, passw=auth.passw))
g.save_file(folder=data[0].strip(), text=data[1])


