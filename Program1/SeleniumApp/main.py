from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import psycopg2
import time

from Program1.Consumer.writer import consumer
from Program1.Producer.kproducer import producer


options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome(options=options)

conn = psycopg2.connect(host="localhost", port="5432", database="app", user="postgres", password="password")


def create_table():
    with conn:
        with conn.cursor() as cur:
            cur.execute('''
                CREATE TABLE IF NOT EXISTS articles (
                    id SERIAL PRIMARY KEY,
                    title TEXT NOT NULL
                )
            ''')


def consume_and_insert_data():
    for message in consumer:
        title = message.value['title']
        with conn:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO articles (title) VALUES (%s)", (title,))
        print('Inserted data:', message.value)


def scrape_and_send_data():
    driver.get('https://svidomi.in.ua/')

    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'newsXCard__wrap')))
    articles = driver.find_elements(By.CLASS_NAME, 'newsXCard__wrap')
    for article in articles:
        title = article.find_element(By.CLASS_NAME, 'newsXCard__title').text
        data = {'title': title}
        producer.send('scraped_data', value=data)
        print(data)


create_table()

while True:
    scrape_and_send_data()

    consume_and_insert_data()

    time.sleep(60)
