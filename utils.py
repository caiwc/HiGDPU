# coding:utf-8
from html.parser import HTMLParser


class myHTMLParser(HTMLParser):
    def __init__(self):
        self.find_content = False
        self.tag = None
        self.l_tag = None
        self.content = []
        super(myHTMLParser, self).__init__()

    def handle_starttag(self, tag, attrs):
        self.l_tag = self.tag
        self.tag = tag
        if tag == 'div':
            for (variable, value) in attrs:
                if variable == 'id' and value == 'js_content':
                    self.find_content = True
        if tag == 'script':
            self.find_content = False

    def handle_data(self, data):
        data = data.strip()
        if not data:
            pass
        elif self.find_content:
            self.content.append(data)


def get_es_data(parser, html):
    parser.feed(html)
    parser.close()

    return " ".join(parser.content)
