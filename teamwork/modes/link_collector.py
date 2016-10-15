import argparse
from bs4 import BeautifulSoup
from collections import defaultdict
import elk
import requests
from teamwork.plugin_bases import ModePlugin


class LinkCollectorPlugin(elk.Elk):
	__with__ = ModePlugin

	def add_parser(self, subparsers):
	    description = "collects links from webpages"
	    parser = subparsers.add_parser('link-collector', description=description, help=description,
	                                   formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	    parser.add_argument('page_address', help="url or similar address of page site")
	    parser.set_defaults(func=self.main)

	def main(self, args):
		data = requests.get(args.page_address).content
		soup = BeautifulSoup(data, 'html.parser')

		links = defaultdict(set)
		for a in soup.find_all('a'):
			# only collect links with titles
			if a.text:
				print(a.text, a.get('href'))
				links[a.text].add(a.get('href'))

