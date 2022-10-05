from config.config import Config

import requests
import time

config = Config()


class WebRequest:
    def requester(self, target_address):
        cookies = config.cookies
        for request_attempt in config.request_sleep_secs:
            time.sleep(3)
            response = requests.get(target_address, cookies=cookies)
            if response.status_code == 200:
                return response
            else:
                print('ERROR: failed to scrape', target_address)
                print('RETRYING IN', request_attempt, 'seconds')
                time.sleep(request_attempt)
        print('ERROR: scraping fail, try again later')
        exit(1)
