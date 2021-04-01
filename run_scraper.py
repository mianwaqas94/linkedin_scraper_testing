from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scraper.spiders.linkedin import LinkedinSpider
import argparse

# Parse command-line arguments.
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument(
    '-u',
    '--user_email',
    required=True,
    help="linkedin login email address")
parser.add_argument(
    '-p',
    '--user_password',
    required=True,
    help="linkedin login password")

args = parser.parse_args()

s = get_project_settings()
proc = CrawlerProcess(s)

user_email = args.user_email
user_passwod = args.user_password

proc.crawl(LinkedinSpider, user_email, user_passwod)
proc.start()
