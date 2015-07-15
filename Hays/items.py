# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HaysItem(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field()
    snippet = scrapy.Field()
    ubicacion = scrapy.Field()
    descripcion = scrapy.Field()
    nombre = scrapy.Field()
    similar = scrapy.Field()
    id = scrapy.Field()
    sector = scrapy.Field()
    pass


class HaysItem_detalle(scrapy.Item):
    # define the fields for your item here like:
    skills_2 = scrapy.Field()
    skills = scrapy.Field()
    ingles = scrapy.Field()
    frances = scrapy.Field()
    espanol = scrapy.Field()
    otro_lenguaje = scrapy.Field()
    trabajo_0 = scrapy.Field()
    trabajo_1 = scrapy.Field()
    trabajo_2 = scrapy.Field()
    trabajo_3 = scrapy.Field()
    trabajo_4 = scrapy.Field()
    education_sum = scrapy.Field()
    education_tot = scrapy.Field()
    full_content = scrapy.Field()
    url = scrapy.Field()
    pass
