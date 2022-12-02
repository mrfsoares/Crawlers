# -*- coding: utf-8 -*-
import pandas as pd
import unicodedata
import scrapy
import re

class UFsSpider(scrapy.Spider):
    '''
    Rode o crawler com o comando >>> scrapy runspider ufs.py <<<.
    '''
    name = 'UFs'
    start_urls = ['https://pt.wikipedia.org/wiki/Lista_de_capitais_do_Brasil_por_%C3%A1rea']
    
    def parse(self, response):
        ref = response.xpath('//*[@id="mw-content-text"]/div[1]/table/tbody/tr')
        df = []
        for valor in ref[1:]:
            ref = {}
            
            sede = valor.xpath('.//td[2]/a/text()').get()
            uf = valor.xpath('.//td[4]/a/text()').get()
            area = unicodedata.normalize('NFKD', valor.xpath('.//td[5]/text()').get())
            area = float(re.sub('[^0-9],', '', area).replace(',', '.').replace(' ', ''))
            
            ref['sede'] = sede
            ref['uf'] = uf
            ref['area (km²)'] = area

            df.append(ref)
            
        df = pd.DataFrame(df)
        print('\n\n', df, '\n\n')
        
        df.to_csv('ufs.csv', sep=';', decimal=',', index=False)
