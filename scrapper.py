# @author Ankit Kumar on 09/10/2018

import scrapy
import json
import codecs
import datetime


class MediumScrapper(scrapy.Spider):
    name = 'medium_scrapper'
    handle_httpstatus_list = [401, 400]

    autothrottle_enabled = True

    searchString = 'Android'

    def writeTofile(fileName, text):
        with codecs.open(fileName, 'w', 'utf-8') as outfile:
            outfile.write(text)

    def start_requests(self):
        start_urls = ['https://www.medium.com/search/posts?q=Data%20Science']

        for url in start_urls:
            yield scrapy.Request(url, 'GET')

    def parse(self, response):
        # writeTofile("Log"+datetime.datetime.now().strftime("%Y%m%d_%H%M%S")+".txt",response.text)
        response_data = response.text
        response_split = response_data.split("while(1);</x>")
        # num_split= len(response_split)
        response_data = response_split[1]
        filename = "medium_" + self.searchString + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + ".json"
        self.writeTofile(filename)

        with codecs.open(filename, 'r', 'utf-8') as infile:
            data = json.load(infile)
        # Check if there is a next tag in json data
        if 'paging' in data['payload']:
            data = data['payload']['paging']
            if 'next' in data:
                # Make a post request
                print "In Paging, Next Loop"
                data = data['next']
                formdata = {
                    'ignoredIds': data['ignoredIds'],
                    'page': data['page'],
                    'pageSize': data['pageSize']
                }
                # cookie = cookie
                #
                # header = header
                yield scrapy.Request('https://www.medium.com/search/posts?q=' + self.searchString, method='POST',
                                     body=json.dumps(formdata), callback=self.parse)
