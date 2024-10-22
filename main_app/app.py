# coding:utf-8

# 必要なパッケージのインポート
import streamlit as st
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome import service as fs
from selenium.webdriver import ChromeOptions
from webdriver_manager.core.os_manager import ChromeType
from selenium.webdriver.common.by import By

# タイトルを設定
st.title("seleniumテストアプリ")

# ボタンを作成(このボタンをアプリ上で押すと"if press_button:"より下の部分が実行される)
press_button = st.button("スクレイピング開始")

if press_button:
    # スクレイピングするwebサイトのURL
    URL = 'https://mynavi-ms.jp/search/fukuoka/area-all/'

    # ドライバのオプション
    options = ChromeOptions()


    # option設定を追加（設定する理由はメモリの削減）
    #options.add_argument("--headless")
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    # webdriver_managerによりドライバーをインストール
    CHROMEDRIVER = ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()
    service = fs.Service(CHROMEDRIVER)
    driver = webdriver.Chrome(
                              options=options,
                              service=service
                             )

    # URLで指定したwebページを開く
    driver.get(URL)
    # クラス名で要素を取得
    job_cards = driver.find_elements(By.XPATH, '//div[@class="job-summary"]/div/h3/a[@target="_blank"]')
    table_cards = driver.find_elements(By.CLASS_NAME, 'job-summary-table')

    print([t.text for t in job_cards])
    print([s.text for s in table_cards])

    st.text(f'job_cards : {job_cards}')
    st.text(f'table_cards : {table_cards}')

    # webページ上のタイトル画像を取得
    img = driver.find_element(By.TAG_NAME, 'img')
    src = img.get_attribute('src')
    st.text(f'img : {img}')

    # 取得した画像をカレントディレクトリに保存
    with open(f"tmp_img.png", "wb") as f:
        f.write(img.screenshot_as_png)

    # 保存した画像をstreamlitアプリ上に表示
    st.image("tmp_img.png")

    # webページを閉じる
    driver.close()

    # スクレピン完了したことをstreamlitアプリ上に表示する
    st.write("スクレイピング完了!!!")