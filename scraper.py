#! usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Rob Spears (GitHub: Forty9Unbeaten)'

import sys
import argparse
import requests
import re


def create_parser():
    parser = argparse.ArgumentParser(
        description='Scrape a website for URLs, email addresses and ' +
                    'phone numbers')
    parser.add_argument('http',
                        help='The address of the site to be scraped')
    return parser


def get_html(web_address):
    web_address = format_address(web_address)
    try:
        r = requests.get(web_address)
    except Exception as e:
        print('Error: {}'.format(e))
    else:
        special_char_regex = r'(\r|\n|\t)'
        html = re.sub(special_char_regex, '', r.text)
        return html


def format_address(address):
    http_regex = r'(https://|http://)\S*'
    valid_address = re.search(http_regex, address)
    if not valid_address:
        address = 'https://{}'.format(address)
    return address


def main(args):
    parser = create_parser()
    if not args:
        print('\n\tPlease supply a web address\n')
        parser.print_help()
        sys.exit()

    address = parser.parse_args().http
    html_text = get_html(address)


if __name__ == '__main__':
    main(sys.argv[1:])
