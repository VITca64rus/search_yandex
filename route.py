from flask import Flask
from flask import request

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options

app = Flask(__name__)


@app.route('/')
def hello():
    find = request.args.get('find')
    if find is None:
        return("Передайте get параметр find. Пример 127.0.0.1:3000/?find=фармстандарт")
    else:
        driver = webdriver.Chrome()
        option = Options()
        option.add_argument("--disable-infobars")
        browser = webdriver.Chrome(executable_path='/home/sazelda/Downloads/chromedriver_linux64(2)/chromedriver', options=option)
        browser.get('https://yandex.ru')
        elem = browser.find_element(By.ID, 'text')
        elem.send_keys(find + Keys.RETURN)
        # time.sleep(4)
        source_data = browser.page_source
        soup = BeautifulSoup(source_data)
        title = soup.find_all(attrs={"class": {"OrganicTitleContentSpan organic__title"}})
        label = soup.find_all(attrs={"class": {"OrganicTextContentSpan"}})
        src = soup.find_all(attrs={"class": {"Path Organic-Path path organic__path"}})

        res = "<table>" \
              "<tr>" \
              "<th>Номер</th>" \
              "<th>Заголовок</th>" \
              "<th>Описание</th>" \
              "<th>Ссылка</th>" \
              "</tr>"
        print(len(title),len(label),len(src))
        for i in range(len(title)):
            if i == 10:
                break
            try:
                res += "<tr>"
                res += "<td>" + str(i + 1) + "</td>"
                res += "<td>" + str(title[i]) + "</td>"
                res += "<td>" + str(label[i]) + "</td>"
                res += "<td>" + str(src[i]) + "</td>"
                res += "</tr>"
            except:
                break
        return res

if __name__ == '__main__':
    app.run(port=3000, debug = True)