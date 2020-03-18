#! usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Rob Spears (GitHub: Forty9Unbeaten)'

import sys
import argparse


def create_parser():
    parser = argparse.ArgumentParser(
        description='Scrape a website for URLs, email addresses and ' +
                    'phone numbers')
    parser.add_argument('http',
                        help='The address of the site to be scraped')
    return parser


def main(args):
    parser = create_parser()

    if not args:
        print('\n\tPlease supply a web address\n')
        parser.print_help()
        sys.exit()


if __name__ == '__main__':
    main(sys.argv[1:])
