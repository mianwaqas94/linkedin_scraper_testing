import scrapy
from scrapy__selenium import SeleniumRequest


class LinkedinSpider(scrapy.Spider):
    name = 'linkedin'
    headers = {
        'authority': 'www.linkedin.com',
        'cache-control': 'max-age=0',
        'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'upgrade-insecure-requests': '1',
        'origin': 'https://www.linkedin.com',
        'content-type': 'application/x-www-form-urlencoded',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'accept-language': 'en-US,en;q=0.9,ru;q=0.8'
    }

    def __init__(self,
                 user_email,
                 password,
                 *args,
                 **kwargs):
        super(LinkedinSpider, self).__init__(*args, **kwargs)

        self.user_email = user_email
        self.password = password

    def start_requests(self):
        """
        Adds the start/seed URLs to the crawl queue.
        """

        sign_in_url = "https://www.linkedin.com/login"
        yield scrapy.Request(
            url=sign_in_url,
            callback=self.login,
            headers=self.headers
        )

    def login(self, response):
        """
        This method logins the linkedin
        """

        return scrapy.FormRequest.from_response(
            response,
            formxpath='//form[@class="login__form"]',
            formdata={'session_key': self.user_email, 'session_password': self.password},
            callback=self.check_login_response)

    def check_login_response(self, response):
        test_query = "https://www.linkedin.com/search/results/people/?currentCompany=%5B%2210667%22%5D&geoUrn=%5B%22103644278%22%5D&keywords=software%20engineer&origin=FACETED_SEARCH&pastCompany=%5B%221035%22%5D"
        yield SeleniumRequest(
            url=test_query,
            callback=self.parse_query_page,
            # TODO: Here we need to send the cookies by  response.headers.getlist('Set-Cookie'), I think we need to parse the cookie string in json
        )

    def parse_query_page(self, response):
        with open('query_response.html', 'w') as f:
            f.write(response.text)
