# -*- coding: utf-8 -*-
#desde workspace

import re
import time
from scrapy.selector import Selector
import scrapy
from selenium import webdriver
from Hays.items import HaysItem, HaysItem_detalle
import pandas as pn
from scrapy import signals
# from selenium.common.exceptions import WebdriverException
# from selenium.common.exceptions import WebdriverException
# from scrapy.http import Request
# from scrapy import Spider
# import urllib2
from selenium import webdriver
KEY = 
def try_item(x):
    try:
        res = x
    except:
        res = None
    return res
from scrapy.http import Request
from scrapy.xlib.pydispatch import dispatcher
#no se bien qué es esto:
#rsid=851944331435297466105&
#obtiene url y nombre de todos los individuos.
#https://www.linkedin.com/vsearch/p?
#keywords=it,%20manager&openAdvancedForm=true&
# locationType=I&countryCode=mx&rsid=851944331435298366307&orig=ADVS
class linkedin_id(scrapy.Spider):
    """ Saving a URL tuple to start"""
    name = "linkedin"
    allowed_domains = ["https://www.linkedin.com"]

    start_urls = ['https://www.linkedin.com/uas/login?session_redirect=https%3A%2F%2Fwww%2Elinkedin%'
                   '2Ecom%2Fvsearch%2Fp%3Fkeywords%3DIT%252C%2Bmanager%26locationType%3DI%26rsid'
                   '%3D851944331435298366307%26orig%3DADVS%26countryCode%3Dmx%26openAdvancedForm%3Dtrue&fromSignIn=']

    def parse(self, response):
        fp = webdriver.FirefoxProfile()
        driver = webdriver.Firefox()

        start_urls = ['https://www.linkedin.com/uas/login?session_redirect=https%3A%2F%2Fwww%2Elinkedin%'
                       '2Ecom%2Fvsearch%2Fp%3Fkeywords%3DIT%252C%2Bmanager%26locationType%3DI%26rsid'
                       '%3D851944331435298366307%26orig%3DADVS%26countryCode%3Dmx%26openAdvancedForm%3Dtrue&fromSignIn=']

        driver.get(start_urls[0])
        driver.find_element_by_id("session_key-login").send_keys("raquel.sanchez@hays.com.mx")
        driver.find_element_by_id("session_password-login").send_keys(KEY)
        bttn = driver.find_element_by_id("btn-primary")
        bttn.click()
        time.sleep(5)
        #necesarias = "IT%2C+manager"#
        necesarias = "it+developer+leader"
        #necesarias = "javascript+backbone"
        lista = ["team leader","java","ecommerce","e-commerce","javascript","javascript+backbone"]

        urls = []
        print "check 1"

        for y in lista:
            url = "https://www.linkedin.com/vsearch/p?" \
                  "keywords={0}%2C+{1}&" \
                  "openAdvancedForm=true&" \
                  "locationType=I&countryCode=mx&" \
                  "rsid=851944331435298366307&orig=ADVS".format(necesarias,y)
            urls.append(url)

        for i in range(len(urls)):
            driver.get(urls[i])
            print "check 2"
            print urls[i]
            time.sleep(5)
            n_profiles = int(re.search("([0-9]*[\.|\,])?([0-9]*[\.|\,])?[0-9]+",
                                       driver.find_element_by_xpath('//div[@class="search-info"]').text).group(0)
                                        .replace(".","").replace(",",""))

            #paginacion
            if n_profiles>=10:
                n_paginas = n_profiles/10
                print n_paginas
                if n_paginas > 100:
                    n_paginas = 99
                else:
                    pass
            else:
                n_paginas = 1

            perfil_dict = {}

            for j in range(1,n_paginas + 1):
                for i in range(1,11):
                    print i
                    try:
                        perfil = driver.find_element_by_xpath('//li[@class="mod result idx{0} people"]'.format(i))
                        url = perfil.find_element_by_class_name("title").get_attribute("href")
                        id = re.search("id=([A-Za-z0-9_-]*)",url).group(1)
                        print id
                        perfil_dict["{0}".format(id)] = {}
                        perfil_dict["{0}".format(id)]["url"] = url
                    except:
                        pass
                    try:
                        nombre = perfil.find_element_by_class_name("title").text
                        perfil_dict["{0}".format(id)]["nombre"] = nombre
                    except:
                        pass

                    try:
                        descripcion = perfil.find_element_by_class_name("description").text
                        perfil_dict["{0}".format(id)]["descripcion"] = descripcion
                    except:
                        pass

                    try:
                        demographic = perfil.find_element_by_class_name("demographic")
                        try:
                            sector = demographic.find_element_by_xpath('//dd[@class=""]').text
                            perfil_dict["{0}".format(id)]["sector"] = sector
                        except:
                            pass
                        try:
                            ubicacion = demographic.find_element_by_xpath('//dd[@class="separator"]').text
                            perfil_dict["{0}".format(id)]["ubicacion"] = ubicacion
                        except:
                            pass
                    except:
                        pass
                    try:
                        snippet = perfil.find_element_by_class_name("snippet").text
                        perfil_dict["{0}".format(id)]["snippet"] = snippet
                    except:
                        pass
                    try:
                        #not working
                        similar = perfil.find_element_by_xpath('//li[@class="similar"]//a').get_attribute("href")
                        perfil_dict["{0}".format(id)]["similar"] = similar
                    except:
                        pass
                try:
                    bttn = driver.find_element_by_xpath('//li[@class="next"]//a[@class="page-link"]')
                    bttn.click()
                    time.sleep(5)
                except:
                    pass

                #temporal
                # a = str(perfil_dict)
                # data = pn.DataFrame.from_dict(perfil_dict).T
                # data["id"] = data.index
                # data.to_csv("linkedin_temp.csv", encoding="utf8", index=False)

            for each in perfil_dict.keys():
                urli = perfil_dict.get(each).get("url")
                similari = perfil_dict.get(each).get("similar")
                nombrei = perfil_dict.get(each).get("nombre")
                descripcioni = perfil_dict.get(each).get("descripcion")
                snippeti = perfil_dict.get(each).get("snippet")
                ubicacioni = perfil_dict.get(each).get("ubicacion")
                yield HaysItem(url=urli,similar=similari,nombre=nombrei,descripcion=descripcioni,
                               snippet=snippeti,ubicacion=ubicacioni)


"""
class linkedin_detalle():
    name = "linkedindetalle"

    allowed_domains = ["century21mexico.com"]
    def parse(self, response):

        item = HaysItem()

        sel = Selector(response)
        #item = CENTURY21Item()
        try:
            item["url"] = response.url
        except:
            pass
        try:
            item["descripcion"] = (sel.xpath("//span[@class='descripcion']").extract()[0].replace('<span class="descripcion">',"").replace("</span>",""))
        except:
            pass
        try:
            item["idinmueble"] = re.search("id=([0-9]*)",response.url).group(1)
        except:
            pass
        try:
            item["direccion"] = (sel.xpath("//span[@class='direccion']").extract()[0].replace('<span class="direccion">',"").replace("</span>",""))
        except:
            pass
        try:
            a = sel.xpath('//span[@class="precio"]').extract()[0]
            #img = sel.xpath('//div[@class="thirdblock"]/div').extract()
        except:
            pass
        try:
            item["precio"] = re.search("\$[\d+,]*",a).group(0).replace(",","").replace("$","")
        except:
            pass
        try:
            caracteristicas = sel.xpath('//div[@class="caracteristicas"]/span/text()').extract()
            for each in caracteristicas:
                if re.search("Edad", each) is not None:
                    item["edad"] = re.search("\d+", each).group(0)
                elif re.search("Niveles", each) is not None:
                    item["nivel"] = re.search("\d+", each).group(0)

                elif re.search("Frente:", each) is not None:
                    item["frente"] = re.search("\d+.?\d*", each).group(0)
                elif re.search("Jard\xedn", each) is not None:
                    item["jardin"] = re.search("[S\xed|No]", each).group(0).replace("í","si")
                elif re.search("Forma", each) is not None:
                    item["forma"] = re.search(": .*", each).group(0)
                else:
                    pass
        except:
            pass
        try:
            latlong = sel.xpath("//script [@type='text/javascript']")[3].extract()
            latlong_ = re.search("\d{2}\.\d*\,-\d{2}\.\d*",latlong).group(0)
            item["latitud"] = re.search("^\d{2}\.\d*",latlong_).group(0)
            item["longitud"] = re.search("-\d{2}\.\d*",latlong_).group(0)
        except:
            pass
        # for each in img:
        #     if re.search("[Rec\xe1maras|Recamaras]", each) is not None:
        #         item["recamaras"] = re.search("div>\d*.?\d+",each).group(0).replace("div>","")
        #     elif re.search("[Ba\xf1os|Banos]", each) is not None:
        #         item["banos"] = re.search("div>\d*.?\d+", each).group(0).replace("div>","")
        #     elif re.search("Estacionamientos", each) is not None:
        #         item["estacionamientos"] = re.search("div>\d*.?\d+", each).group(0).replace("div>","")
        #     elif re.search("Metros Cuadrados de Terreno", each) is not None:
        #         item["m2terreno"] = re.search("div>\d*.?\d+", each).group(0).replace("div>","")
        #     elif re.search("[Metros Cuadrados de Construcci\xf3n|Metros Cuadrados de Construccion]", each) is not None:
        #         item["m2construidos"] = re.search("div>\d*.?\d+", each).group(0).replace("div>","")
        try:
            nombres=sel.xpath('//div[@class="thirdblock"]/div/span/@title').extract()
            img = sel.xpath('//div[@class="thirdblock"]/div/text()').extract()
            for nombresj, imgi in zip(nombres,img):
                if (nombresj == u"Rec\xe1maras") or (nombresj == u"Recamaras"):
                    item["recamaras"] = imgi
                elif (nombresj == u"Ba\xf1os") or (nombresj == u"Banos"):
                    item["banos"] = imgi
                elif (nombresj == u"Estacionamientos") or (nombresj == u"estacionamientos"):
                    item["estacionamientos"] = imgi
                elif nombresj == u"Metros Cuadrados de Terreno":
                    item["m2terreno"] = imgi
                elif (nombresj == u"Metros Cuadrados de Construcci\xf3n") or (nombresj == u"Metros Cuadrados de Construccion"):
                    item["m2construidos"] = imgi
                else:
                    pass
        except:
            pass

        return item
"""
