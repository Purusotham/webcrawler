import urllib.request
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from html.parser import HTMLParser
from traceback import format_exc
from re import match as re_match
from urllib.request import urlopen

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

    def validate_web_url(self, url):
        """Validate Web URL"""
        try:
            urlopen(url)
            return url
        except Exception as error:
            return ''



class WebCrawler:
    def __init__(self, base_url, depth=1):
        self.base_url = base_url
        self.depth = depth

    def spiderbot(self):
        try:
            # Validations
            if Commons().validate_web_url(self.base_url):
                return {'status_id': 0,
                        'reason': 'Please enter a valid url'}
            if self.depth < 1:
                return {'status_id': 0,
                        'reason': 'Please enter a depth greater than 0'}
            # For URLs
            result_url_dict = {}

            # For images
            result_img_set = set()

            url_list_iterate = [self.base_url]

            for depth in range(self.depth):

                new_list_iterate = []

                for url in url_list_iterate:
                    self.parse_html_from_url(url,
                                             depth + 1,
                                             result_url_dict,
                                             result_img_set,
                                             new_list_iterate)

                url_list_iterate = new_list_iterate
            return {'status_id': 1,
                    'images': list(result_img_set),
                    'urls': result_url_dict}
        except Exception as error:
            print('Exception in parse_html. .:' + str(error))
            print(format_exc().splitlines())
            return {'status_id': 0,
                    'images': {},
                    'urls': []}

    def parse_html_from_url(self, web_url, depth, url_dict, img_list, new_list):
        """Parse web page
        :return:
        """
        try:
            if Commons().validate_web_url(web_url):
                html_string = str(urllib.request.urlopen(web_url).read())
                parser = HTMLStringParser(web_url, depth, url_dict=url_dict, img_list=img_list, url_list=new_list)
                parser.feed(html_string)
        except Exception as error:
            print(web_url)
            # import pdb;pdb.set_trace()
            # print('exception in get_html_from_url....:' + str(error))
            # print(format_exc().splitlines())
            return {'status_id': 0,
                    'reason': 'Failed while parsing URL'}


class HTMLStringParser(HTMLParser):
    """Parse html String"""
    def __init__(self, base_url, depth, url_dict=dict(), img_list=set(), url_list=list()):
        HTMLParser.__init__(self)
        self.base_url = base_url
        self.url_dict = url_dict
        self.url_list = url_list

        self.img_list = img_list
        self.depth = depth

    def handle_starttag(self, tag, attrs):
        attributes_dict = dict(attrs)
        if tag == 'a':
            valid_url = self.restructured_url(attributes_dict.get('href'))
            if valid_url and not self.url_dict.get(valid_url):
                self.url_dict[valid_url] = self.depth
                self.url_list.append(valid_url)
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


