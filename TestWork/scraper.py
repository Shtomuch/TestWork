import json
import logging
import time
import csv
import random

import schedule
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def load_config(config_file='config.json'):
    """Loads the configuration file."""
    with open(config_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def setup_logging(log_file):
    """Sets up logging to a file and the console."""
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    # Additionally output logs to the console
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)


def get_driver(proxy_settings):
    """Configures and returns a Chrome WebDriver with options."""
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--proxy-server='direct://'")
    chrome_options.add_argument("--proxy-bypass-list=*")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--disable-browser-side-navigation")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")

    if proxy_settings['enabled'] and proxy_settings['proxy_list']:
        proxy = random.choice(proxy_settings['proxy_list'])  # Select a random proxy
        chrome_options.add_argument(f'--proxy-server={proxy}')
        logging.info(f"Using proxy: {proxy}")
    else:
        logging.info("Proxy is not being used.")

    driver = webdriver.Chrome(options=chrome_options)

    # Add JavaScript to hide the navigator.webdriver property
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
        'source': '''
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            })
        '''
    })

    return driver


def scrape_data(config):
    """Function to scrape data from the website."""
    logging.info("Starting data scraping.")
    driver = None
    try:
        driver = get_driver(config['proxy'])
        driver.get('https://defillama.com/chains')

        wait = WebDriverWait(driver, 30)
        try:
            header_div = wait.until(EC.presence_of_element_located((By.ID, 'table-header')))
            header_cells = header_div.find_elements(By.CSS_SELECTOR, 'div[data-chainpage]')
        except TimeoutException:
            logging.error("Failed to find 'table-header' after 30 seconds of waiting.")
            logging.debug(driver.page_source)
            return

        headers = []
        for header in header_cells:
            if header.find_elements(By.TAG_NAME, 'button'):
                header_text = header.find_element(By.TAG_NAME, 'button').text.strip()
            else:
                header_text = header.text.strip()
            headers.append(header_text)

        logging.info(f"Table headers: {headers}")

        data = []
        processed_names = set()
        scroll_pause_time = config.get('scroll_pause_time', 1.5)
        scroll_increment = config.get('scroll_increment', 1000)
        scroll_position = 0
        max_attempts = config.get('max_attempts', 5)
        attempts = 0

        while True:

            scroll_position += scroll_increment
            driver.execute_script(f"window.scrollTo(0, {scroll_position});")
            time.sleep(scroll_pause_time)
            row_divs = driver.find_elements(By.CSS_SELECTOR,'#table-wrapper div[style*="position: absolute"][style*="display: flex"]')
            for row in row_divs:
                try:
                    cells = row.find_elements(By.CSS_SELECTOR, 'div[data-chainpage]')
                    if not cells:
                        continue

                    name_element = cells[0].find_element(By.CSS_SELECTOR, 'a.text-sm.font-medium')
                    name = name_element.text.strip()

                    if name in processed_names:
                        continue
                    processed_names.add(name)

                    protocols = cells[1].text.strip() if len(cells) > 1 else ''
                    tvl = cells[6].text.strip() if len(cells) > 6 else ''

                    piece_of_data = {
                        'Name': name,
                        'Protocols': protocols,
                        'TVL': tvl.replace(',', '.')
                    }


                    data.append(piece_of_data)
                    logging.info(f"Collected data: {piece_of_data}")
                except NoSuchElementException:
                    continue


            new_height = driver.execute_script("return document.body.scrollHeight")
            current_scroll = driver.execute_script("return window.pageYOffset + window.innerHeight;")
            if current_scroll >= new_height:
                attempts += 1
                logging.info(f"Reached the end of the page. Attempt {attempts}/{max_attempts}.")
                if attempts >= max_attempts:
                    logging.info("Maximum number of attempts reached. Ending scraping.")
                    break
            else:
                attempts = 0

        logging.info(f'Found {len(data)} rows.')

        output_format = config.get('output_format', 'json').lower()
        output_file = config.get('output_file', 'chains_data.json')
        if output_format == 'json':
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            logging.info(f'Data scraped and saved to {output_file}.')
        elif output_format == 'csv':
            if data:
                keys = data[0].keys()
                with open(output_file, 'w', newline='', encoding='utf-8') as f:
                    dict_writer = csv.DictWriter(f, fieldnames=keys)
                    dict_writer.writeheader()
                    dict_writer.writerows(data)
                logging.info(f'Data scraped and saved to {output_file}.')
            else:
                logging.warning("No data to write to CSV file.")
        else:
            logging.error(f"Unknown output format: {output_format}. Defaulting to JSON.")
            with open('chains_data.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            logging.info('Data scraped and saved to chains_data.json.')

    except Exception as e:
        logging.error(f"An error occurred during scraping: {e}")
    finally:
        if driver:
            driver.quit()
        logging.info("Data scraping completed.")


def main():
    """Main function to set up and run the scraper."""
    config = load_config()
    setup_logging(config.get('log_file', 'scraping.log'))
    interval = max(1, config.get('scrape_interval_minutes', 5))
    schedule.every(interval).minutes.do(scrape_data, config=config)
    logging.info(f"Data scraping scheduled every {interval} minutes.")
    scrape_data(config)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
