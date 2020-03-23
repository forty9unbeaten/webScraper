#! usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Rob Spears (GitHub: Forty9Unbeaten)'

import sys
import argparse
import requests
import re
import os


def create_parser():
    '''Creates a shell argument parser and returns the parser object'''
    parser = argparse.ArgumentParser(
        description='Scrape a website for URLs, email addresses and ' +
                    'phone numbers')
    parser.add_argument('http',
                        help='The address of the site to be scraped')
    return parser


def get_html(web_address):
    '''Retrieves raw html text from a particular webpage and returns it'''
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
    '''Formats a web address to include "http://" or "https://" as necessary'''
    http_regex = r'(https://|http://)\S*'
    valid_address = re.search(http_regex, address)
    if not valid_address:
        address = 'https://{}'.format(address)
    return address


def find_urls(raw_html):
    '''Finds and returns list of urls contained in raw html from a webpage'''
    url_regex = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    return list(set(re.findall(url_regex, raw_html)))


def find_emails(raw_html):
    '''Finds and returns a list of email addresses
     contained in raw html from a webpage'''
    email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    return list(set(re.findall(email_regex, raw_html)))


def find_phone_nums(raw_html):
    '''Finds and returns a list of phone numbers
     contained in raw html from a webpage'''
    phone_num_regex = r'1?\W*([2-9][0-8][0-9])\W*([2-9][0-9]{2})\W*([0-9]{4})(\se?x?t?(\d*))?'
    return list(set(re.findall(phone_num_regex, raw_html)))


def main(args):
    parser = create_parser()
    if not args:
        print('\n\tPlease supply a web address\n')
        parser.print_help()
        sys.exit()

    address = parser.parse_args().http
    html_text = get_html(address)

    # find and URLs, email addresses and phone numbers
    # contained in html
    urls = find_urls(html_text)
    emails = find_emails(html_text)
    phone_nums = find_phone_nums(html_text)


if __name__ == '__main__':
    main(sys.argv[1:])
