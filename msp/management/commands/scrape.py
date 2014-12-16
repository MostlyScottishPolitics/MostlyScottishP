__author__ = 'laura'

from scraper.report_scraper import retriever
from django.core.management.base import NoArgsCommand


class Command(NoArgsCommand):

    help = 'Scrape data'

    def handle_noargs(self, **options):
        retriever.scrap_files(retriever.get_html_files())
