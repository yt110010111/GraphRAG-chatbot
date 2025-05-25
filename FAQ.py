from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

def main():
    url = "https://www.esunbank.com/zh-tw/about/faq"

    options = Options()
    options.add_argument('--headless')  # 不開啟視窗背景執行
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')

    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)
        time.sleep(5)  # 等待 JS 動態載入，視網速可調整

        # FAQ 問答區塊
        faqs = driver.find_elements(By.CLASS_NAME, "accordion-group")
        print(f"總共找到 {len(faqs)} 組問答")

        for i, faq in enumerate(faqs, 1):
            question = faq.find_element(By.CLASS_NAME, "title").text.strip()
            answer = faq.find_element(By.CLASS_NAME, "content").text.strip()
            print(f"問題 {i}: {question}")
            print(f"答案 {i}: {answer}")
            print("-" * 50)

    except Exception as e:
        print(f"發生錯誤：{e}")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
