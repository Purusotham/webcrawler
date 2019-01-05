import urllib.request
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from html.parser import HTMLParser
from traceback import format_exc
from re import match as re_match


class Commons:
    def __init__(self):
        pass

    def validate_url(self, url):
        """Validate url
        :param url:
        :return:
        """
        try:
            validate = URLValidator()
            validate(url)
            return url
        except ValidationError:
            return ''


class WebCrawler:
    def __init__(self, base_url, depth=0):
        self.base_url = base_url
        self.depth = depth

    def parse_html(self):
        try:
            result_url_dict = {}
            result_img_list = set()
            # if self.depth:

            self.parse_html_from_url(self.base_url, self.depth, result_url_dict, result_img_list)

            return {'status_id': 1,
                    'images': result_url_dict,
                    'urls': list(result_img_list)}
        except Exception as error:
            print('Exception in parse_html..:' + str(error))

    def parse_html_from_url(self, web_url, depth, url_dict, img_list):
        """Parse web page
        :return:
        """
        try:
            if Commons().validate_url(web_url):
                html_string = str(urllib.request.urlopen(web_url).read())
                parser = HTMLStringParser(web_url, depth, url_dict=url_dict, img_list=img_list)
                parser.feed(html_string)
                # images = parser.img_list
                # urls = parser.url_dict
                # return {'status_id': 1,
                #         'images': list(images),
                #         'urls': list(urls)}
            # else:
            #     return {'status_id': 0,
            #             'reason': 'Invalid URL'}
        except Exception as error:
            print('exception in get_html_from_url....:' + str(error))
            print(format_exc().splitlines())
            return {'status_id': 0,
                    'reason': 'Failed while parsing URL'}


class HTMLStringParser(HTMLParser):
    """Parse html String"""
    def __init__(self, base_url, depth, url_dict=dict(), img_list=set()):
        HTMLParser.__init__(self)
        self.base_url = base_url
        self.url_dict = url_dict
        self.img_list = img_list
        self.depth = depth

    def handle_starttag(self, tag, attrs):
        attributes_dict = dict(attrs)
        if tag == 'a' and not self.url_dict.get(attributes_dict.get('href')):
            valid_url = self.restructured_url(attributes_dict.get('href'))
            if valid_url:
                self.url_dict[valid_url] = self.depth
        if tag == 'img':
            valid_url = self.restructured_url(attributes_dict.get('src'))
            if valid_url:
                self.img_list.add(valid_url)

    def restructured_url(self, url):
        if re_match('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', url):
            if Commons().validate_url(url):
                return url
        else:
            url = self.base_url + \
                  ('' if url[0] == '/' else '/') + url
            if Commons().validate_url(url):
                return url


