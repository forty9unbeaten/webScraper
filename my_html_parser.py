from html.parser import HTMLParser


class HTMLScraper(HTMLParser):
    urls = []

    def handle_starttag(self, tag, attrs):
        if tag == 'img' and attrs:
            for attribute in attrs:
                if attribute[0] == 'src':
                    self.urls.append(attribute[1])
        elif tag == 'a' and attrs:
            for attribute in attrs:
                if attribute[0] == 'href':
                    self.urls.append(attribute[1])
