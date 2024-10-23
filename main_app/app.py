from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from webdriver_manager.core.os_manager import ChromeType

# ChromeDriverのパスを取得
driver_path = ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()

# サービスオブジェクトを作成
service = ChromeService(executable_path=driver_path)

# Chromeブラウザを起動する際に、サービスを指定
browser = webdriver.Chrome(service=service)

# ここからブラウザ操作を続ける...
browser.get('https://mynavi-ms.jp/search/fukuoka/area-all/')

sleep(4)
print('HERE')

