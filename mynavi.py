import os
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.webdriver import WebDriver
import time
import datetime
import pandas as pd

# Chromeを起動する関数


def set_driver(driver_path, headless_flg):
    # Chromeドライバーの読み込み
    options = ChromeOptions()

    # ヘッドレスモード（画面非表示モード）をの設定
    if headless_flg == True:
        options.add_argument('--headless')

    # 起動オプションの設定
    options.add_argument(
        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36')
    # options.add_argument('log-level=3')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--incognito')          # シークレットモードの設定を付与

    # ChromeのWebDriverオブジェクトを作成する。
    return Chrome(executable_path=os.getcwd() + "/" + driver_path, options=options)

# main処理


def find_table_target_word(th_elms, td_elms, target: str):
    # tableのthからtargetの文字列を探し一致する行のtdを返す
    for th_elm, td_elm in zip(th_elms, td_elms):
        if th_elm.text == target:
            return td_elm.text


def main():
    search_keyword = input("検索キーワードを入力してください：")
    # driverを起動
    if os.name == 'nt':  # Windows
        driver = set_driver("chromedriver.exe", False)
    elif os.name == 'posix':  # Mac
        driver = set_driver("chromedriver", False)
    # Webサイトを開く
    driver.get("https://tenshoku.mynavi.jp/")
    time.sleep(5)

    try:
        # ポップアップを閉じる
        driver.execute_script('document.querySelector(".karte-close").click()')
        time.sleep(5)
        # ポップアップを閉じる
        driver.execute_script('document.querySelector(".karte-close").click()')
    except:
        pass

    # 検索窓に入力
    driver.find_element_by_class_name(
        "topSearch__text").send_keys(search_keyword)
    # 検索ボタンクリック
    driver.find_element_by_class_name("topSearch__button").click()

    # ページ終了まで繰り返し取得
    exp_name_list = []
    exp_copy_list = []
    exp_status_list = []
    exp_first_year_fee_list = []
    # 検索結果の一番上の会社名を取得
    name_list = driver.find_elements_by_css_selector(
        ".cassetteRecruit__heading .cassetteRecruit__name")
    copy_list = driver.find_elements_by_css_selector(
        ".cassetteRecruit__heading .cassetteRecruit__copy")
    status_list = driver.find_elements_by_css_selector(
        ".cassetteRecruit__heading .labelEmploymentStatus")
    table_list = driver.find_elements_by_css_selector(
        ".cassetteRecruit .tableCondition")  # 初年度年収
    # 1ページ分繰り返し
    print(len(name_list))
    print(len(copy_list))
    print(len(status_list))
    print(len(table_list))
    for name, copy, status, table in zip(name_list, copy_list, status_list, table_list):
        exp_name_list.append(name.text)
        exp_copy_list.append(copy.text)
        exp_status_list.append(status.text)
        # 初年度年収をtableから探す
        first_year_fee = find_table_target_word(table.find_elements_by_tag_name(
            "th"), table.find_elements_by_tag_name("td"), "初年度年収")
        exp_first_year_fee_list.append(first_year_fee)
# CSV出力
    now = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    df = pd.DataFrame({"企業名": exp_name_list,
                       "キャッチコピー": exp_copy_list,
                       "ステータス": exp_status_list,
                       "初年度年収": exp_first_year_fee_list})

    df.to_csv('求人情報.csv', index=False)
    driver.quit()


# 直接起動された場合はmain()を起動(モジュールとして呼び出された場合は起動しないようにするため)
if __name__ == "__main__":
    main()
