# coding:utf-8
import streamlit as st
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome import service as fs
from selenium.webdriver import ChromeOptions

# タイトルを設定
st.title("seleniumテストアプリ")

# スクレイピングするwebサイトのURL
URL = "https://ohenziblog.com"

# webdriver_managerによりドライバーをインストール
CHROMEDRIVER = ChromeDriverManager().install()
service = fs.Service(CHROMEDRIVER)
driver = webdriver.Chrome(
                          service=service
                         )

# URLで指定したwebページを開く
driver.get(URL)

# webページを閉じる
driver.close()

# スクレピン完了したことをstreamlitアプリ上に表示する
st.write("selenium終了")