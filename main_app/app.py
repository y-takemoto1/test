# coding:utf-8

# 必要なパッケージのインポート
import streamlit as st
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome import service as fs
from selenium.webdriver import ChromeOptions
from webdriver_manager.core.os_manager import ChromeType
from selenium.webdriver.common.by import By
import time
import re
import openpyxl
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from io import BytesIO

# タイトルを設定
st.title("seleniumテストアプリ")

url = 'https://jp.indeed.com/jobs?q=%E6%AD%A3%E7%A4%BE%E5%93%A1&l=%E7%A6%8F%E5%B2%A1%E7%9C%8C&from=searchOnDesktopSerp&vjk=d4bb56841be7498e'

# 初期の値を表示するための空の場所を作成
text_placeholder = st.empty()

# 初期化
if 'stop' not in st.session_state:
    st.session_state.stop = False
if 'processing' not in st.session_state:
    st.session_state.processing = False

# エクセルを開く
wb = openpyxl.Workbook()
ws = wb.active

# ボタンを作成(このボタンをアプリ上で押すと"if press_button:"より下の部分が実行される)
press_button = st.button("スクレイピング開始")

if press_button:
    # スクレイピングするwebサイトのURL
    URL = url

    # ドライバのオプション
    options = ChromeOptions()

    # option設定を追加（設定する理由はメモリの削減）
    options.add_argument("--headless")
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
    # ページが読み込まれるのを待つ
    time.sleep(15)

    if url:
        # ステータスコードをチェック
        st.text('ルート確認3')
        c = 1  # 行数
        j = 1  # ページ数
        while c <= 10:
            print(f'Processing page {j}...')
            st.text('ルート確認4')
            # 求人情報の取得

            # webページ上のタイトル画像を取得
            img = driver.find_element(By.TAG_NAME, 'img')
            st.text(img)
            st.image(img)
            src = img.get_attribute('src')

            # 取得した画像をカレントディレクトリに保存
            with open(f"tmp_img.png", "wb") as f:
                f.write(img.screenshot_as_png)

            # 保存した画像をstreamlitアプリ上に表示
            st.image("tmp_img.png")

            job_cards = driver.find_element(By.ID, "FindJobs")
            st.experimental_fragment(job_cards)

            if not job_cards:
                st.text('求人が見つかりませんでした。')
                break
            for job in job_cards:
                st.text('testcount:', c)
                st.text('ルート確認5')
                if st.session_state.stop:
                    st.session_state.running = False
                    st.warning("処理が中断されました。")
                    break

                # プレースホルダーに新しいテキストを表示
                text_placeholder.text(f'読込数：{c}')

                # 求人タイトルを取得
                title = job.find_element(By.TAG_NAME, 'title').text.strip()
                st.text('求人タイトル:', title)
                
                # 会社名を取得
                company = job.find_element(By.ID, 'company-name').text.strip()
                st.text('会社名:', company)

                # 詳細ページのリンクを取得
                job_link = 'https://mynavi-ms.jp/' + job.find('a')['href']

                # 待機
                time.sleep(10)
                # 詳細ページにリクエストを送信
                job_response = driver.get(job_link)

                # 勤務地を取得
                location = job.find_element(By.ID, 'jobLocationText').text.strip()
                st.text('勤務地：', location)

                # 仕事内容
                job_description = job.find_element(By.TAG_NAME, 'JobDescription')
                st.text('仕事内容：', job_description)

                # 電話番号を含む要素を取得
                text_elements = driver.find_elements(By.CSS_SELECTOR, '.phone')  # 適切なセレクタを使用
                all_text = ' '.join([element.text for element in text_elements])
                # 正規表現で電話番号を抽出
                phone_numbers = re.findall(r'\b\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{4}\b', all_text)
                phone_numbers2 = [number for number in phone_numbers if not number.startswith("0120")]
                if phone_numbers2:
                    st.text('電話番号:', phone_numbers)
                    # Excelファイルに書き込mi 
                    ws.cell(row=c, column=1, value=title)
                    ws.cell(row=c, column=2, value=company)
                    ws.cell(row=c, column=3, value=', '.join(phone_numbers) if phone_numbers else 'なし')
                    ws.cell(row=c, column=4, value=location)
                    ws.cell(row=c, column=5, value=job_description)
                    c += 1
                else:
                    st.text('電話番号は見つかりませんでした。')
                driver.back()
                print('-' * 40)
                WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "jobTitle css-1psdjh5 eu4oa1w0"))
                )
                time.sleep(1) 

            # 次のページを探す
            next_page = driver.find_element(By.TAG_NAME, 'Next Page')
            if next_page and 'href' in next_page.attrs:
                next_url = 'https://mynavi-ms.jp' + next_page['href']
                driver = driver.get(next_url)
                time.sleep(5)  # サーバーへの負荷を避けるためにスリープ
                j += 1
            else:
                st.text('pageEnd')
                break  # 次のページがない場合は終了
        else:
            st.text('完了しました。')
            #st.text("C:/aggregate/に保存されました。")
    else:
        st.text('リクエストが失敗しました。ステータスコード')


    # webページを閉じる
    driver.close()

    # Excelファイルをメモリに保存
    excel_buffer = BytesIO()
    wb.save(excel_buffer)
    wb.close()
    excel_buffer.seek(0)

    # ダウンロードボタンを表示
    st.download_button(label="Download Excel", data=excel_buffer, file_name='app.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    # スクレピン完了したことをstreamlitアプリ上に表示する
    st.write("スクレイピング完了!!!")
# エクセルファイルを保存
wb.save("app.xlsx")
wb.close()



if st.button("中断", disabled=st.session_state.processing):
    st.session_state.stop = True