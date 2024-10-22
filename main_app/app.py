from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# ChromeDriverのパスを取得
service = ChromeService(ChromeDriverManager().install())

# Chromeブラウザを起動
driver = webdriver.Chrome(service=service)

driver.implicitly_wait(5)
driver.get('https://mynavi-ms.jp/search/fukuoka/area-all/')

# クラス名で要素を取得
job_cards = driver.find_elements(By.XPATH, '//div[@class="job-summary"]/div/h3/a[@target="_blank"]')
table_cards = driver.find_elements(By.CLASS_NAME, 'job-summary-table')

# 要素のテキストを表示
print([t.text for t in job_cards])
print([s.text for s in table_cards])

# ブラウザを閉じる
driver.quit()
