#! usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Rob Spears (GitHub: Forty9Unbeaten)'

import sys
import argparse
import requests
import re
from my_html_parser import HTMLScraper


def create_parser():
    '''Creates a shell argument parser and returns the parser object'''
    parser = argparse.ArgumentParser(
        description='Scrape a website for URLs, email addresses and ' +
                    'phone numbers')
    parser.add_argument('http',
                        help='The address of the site to be scraped')
    parser.add_argument('-d', '--todir',
                        help='Name of the .txt file to write results ' +
                        ' (defaults to output.txt)',
                        default='output.txt',
                        dest='todir')
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

    # find URLs directly in HTML with regex
    url_regex = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    urls = re.findall(url_regex, raw_html)

    # find relative URLs in 'img' and 'a' tag attributes
    scraper = HTMLScraper()
    scraper.feed(raw_html)

    urls = list(set(urls + scraper.urls))
    return sorted(urls)


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


def write_to_file(urls, emails, phone_numbers, filename):
    '''Create and write urls, emails and phone numbers to a
     text file with name {filename}'''
    with open(filename, 'w') as f:
        if urls:
            f.write('URLs:\n\n')
            f.write('\n'.join(urls))
        if emails:
            f.write('\n\nEMAIL ADDRESSES:\n\n')
            f.write('\n'.join(emails))
        if phone_numbers:
            f.write('\n\nPHONE NUMBERS:\n\n')
            for num in phone_numbers:
                f.write('({}) {}-{}\n'.format(num[0], num[1], num[2]))


def main(args):
    parser = create_parser()

    # check that args are provided
    if not args:
        print('\n\tPlease supply a web address\n')
        parser.print_help()
        sys.exit()

    ns = parser.parse_args()

    # check that file to which results will be written is
    # a .txt file
    txt_file_regex = r'\.txt\Z'
    is_txt_file = re.search(txt_file_regex, ns.todir)
    if not is_txt_file:
        print('\n\tOutput file must be a .txt file\n')
        sys.exit()

    html_text = get_html(ns.http)

    # exit program if no html is returned from address provided
    if not html_text:
        print('\n\tNo HTML was returned from the address you provided. ' +
              'Try again with the following address format: www.domain.com\n')
        sys.exit()

    # find and URLs, email addresses and phone numbers
    # contained in html
    urls = find_urls(html_text)
    emails = find_emails(html_text)
    phone_nums = find_phone_nums(html_text)

    # write search results to text file
    write_to_file(urls, emails, phone_nums, ns.todir)


if __name__ == '__main__':
    main(sys.argv[1:])
