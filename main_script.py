# main_script.py

from scrape_links import get_links
from scrape_articles import get_articles
from settings import *

links_df = get_links(url, start_page, end_page)
articles_df = get_articles(links_df)

articles_df.to_csv('Scraped_Al_Jazeera_articles.csv')
