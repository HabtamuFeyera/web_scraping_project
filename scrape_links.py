from bs4 import BeautifulSoup
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.webdriver import WebDriver as ChromeWebDriver
import pandas as pd

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_links(url, start_page, end_page):
    driver = None
    try:
        chrome_options = ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--headless')

        driver = ChromeWebDriver(options=chrome_options)
        driver.get(url)
        driver.maximize_window()

        # Wait for the element with ID 'ensCloseBanner' to be clickable
        wait = WebDriverWait(driver, 10)
        close_banner = wait.until(EC.element_to_be_clickable((By.ID, 'ensCloseBanner')))
        close_banner.click()

        number = 1
        links = []

        for i in range(0, end_page):
            driver.find_element_by_link_text(str(number)).click()
            print('clicked page', number)
            driver.implicitly_wait(10)

            if number >= start_page and number <= end_page:
                html = driver.page_source
                html = BeautifulSoup(html, "lxml")
                articles = html.find_all('div', {'class': 'col-sm-7 topics-sec-item-cont'})

                for article in articles:
                    ankor_list = article.findChildren('a')
                    for ankor in ankor_list:
                        url = ankor.get('href')
                        url = 'https://www.aljazeera.com' + url
                        if 'news' in url or 'opinion' in url:
                            links.append(url)
                            print(url)

                number = number + 1
            elif number < start_page:
                number = number + 4
            else:
                break

        links_df = pd.DataFrame({'links': links})
        links_df = links_df.drop_duplicates(subset='links', keep='last', inplace=False)
        return links_df

    except Exception as e:
        print(e)

    finally:
        if driver:
            driver.quit()
            print('Finished.')
