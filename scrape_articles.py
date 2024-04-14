import newspaper
from newspaper import Article
import pandas as pd
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.webdriver import WebDriver as ChromeWebDriver


def get_articles(df):
    driver = None
    try:
        chrome_options = ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--headless')

        driver = ChromeWebDriver(options=chrome_options)
        urls = []
        headers = []
        texts = []

        for url in df['links']:
            try:
                article = Article(url)
                article.download()
                article.parse()
                print(article.title)

                urls.append(url)
                headers.append(article.title)
                texts.append(article.text)
                driver.implicitly_wait(5)
            except Exception as article_error:
                print(f"Error occurred for article URL: {url}")
                print(f"Error message: {article_error}")

        articles_df = pd.DataFrame({'url': urls, 'title': headers, 'text': texts})
        return articles_df

    except Exception as e:
        print(f"An error occurred: {e}")
        return pd.DataFrame(columns=['url', 'title', 'text'])  # Return an empty DataFrame

    finally:
        if driver:
            driver.quit()
            print('Finished.')
