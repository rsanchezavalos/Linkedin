# -*- coding: utf-8 -*-
__author__ = 'rsanchez'

#urls_linkedin_temp.json - crawler info
#workspace/Hays/Hays/urls_linkedin.json
#linkedin tiene todos los intros
#workspace/Hays/Hays/linkedin_detalle.json
#detalle tiene todos los perfiles más los ocultos con None
#al entrar nuevos busca si estan en intros y si no agrega, luego busca
#si estan en detalle y si no n
import re
import pandas as pn
import time
from selenium import webdriver
from Hays.items import HaysItem, HaysItem_detalle
from selenium import webdriver
from string import lower



def login_linkedin(mail="raquel.sanchez@hays.com.mx",key="Rnnm345R"):
    """
        Saving a URL tuple to start
    """
    fp = webdriver.FirefoxProfile()
    driver = webdriver.Firefox(firefox_profile=fp)
    start_urls = ['https://www.linkedin.com/uas/login?session_redirect=https%3A%2F%2Fwww%2Elinkedin%'
                   '2Ecom%2Fvsearch%2Fp%3Fkeywords%3DIT%252C%2Bmanager%26locationType%3DI%26rsid'
                   '%3D851944331435298366307%26orig%3DADVS%26countryCode%3Dmx%26openAdvancedForm%3Dtrue&fromSignIn=']
    driver.get(start_urls[0])
    time.sleep(10)
    driver.find_element_by_id("session_key-login").send_keys(mail)
    driver.find_element_by_id("session_password-login").send_keys(key)
    time.sleep(10)
    bttn = driver.find_element_by_id("btn-primary")
    bttn.click()
    return driver
def try_item(x):
    try:
        res = x
    except:
        res = None
    return res
def add_new_url_list(new):
    old = pn.read_json("urls_linkedin.json")
    new = pn.read_json(new)
    data = old.append(new)
    data.drop_duplicates(inplace=True,take_last=True)
    data.reset_index(drop=True,inplace=True)
    data.to_json("urls_linkedin.json")
    return "new urls added"

def obtain_url_list():
    sum = pn.read_json("urls_linkedin.json")
    urls_sum = sum["url"].tolist()

    detalle = pn.read_json("linkedin_detalle")
    urls_detalle = detalle["url"].tolist()

    url = []
    for each in urls_sum:
        if each not in urls_detalle:
             url.append(each)
    return url

def get_profile_data(driver,url):
    driver.get(url)
    time.sleep(5)
    item = HaysItem_detalle()
    try:
        item["url"] = url
        try:
            driver.find_element_by_class_name("more-text").click()
        except:
            pass
        try:
            full_content = driver.find_element_by_class_name("background-content ").text
        except:
            pass
        #past experience
        past = driver.find_elements_by_xpath('//div[@id="background-experience"]//div[@class="editable-item section-item past-position"]')

        i = 0
        for each in past:
            try:
                child = each.find_element_by_class_name('education-associated')
                string = each.text.replace(child.text, '')
                full_content = full_content.replace(child.text, '')
            except:
                string = each.text
            item["trabajo_{0}".format(i)] = string
            i += 1
            if i>4:
                break
        item["full_content"] = full_content
        #skills
        try:
            item["skills"] = driver.find_element_by_class_name("skills-section").text
            item["skills_2"] = driver.find_element_by_css_selector(".compact-view").text
        except:
            pass

        #education
        try:
            item["education_sum"] = driver.find_element_by_id("overview-summary-education").text
            item["education_tot"] = driver.find_element_by_id("background-education").text
        except:
            pass

        try:
            languages =  driver.find_element_by_id("languages").find_elements_by_class_name("section-item")
            for each in languages:
                language = try_item(each.find_element_by_tag_name("span").text)
                proficiency = try_item(each.find_element_by_class_name("languages-proficiency").text)
                if language == u'Ingl\xe9s':
                    item["ingles"] = try_item(proficiency)
                elif language == u'Franc\xe9s':
                    item["frances"] = try_item(proficiency)
                elif language == u'Espa\xf1ol':
                    item["espanol"] = try_item(proficiency)
                else:
                    item["otro_lenguaje"] = try_item(language + proficiency)
        except:
            pass

        try:
            item["personal"] = driver.find_element_by_id("personal-info-view").text
        except:
            pass
        return item
    except:
        item = {"url":url,'trabajo_1':None,'trabajo_0':None,'education_sum':None,'skills':None,'full_content':None,'education_tot':None,'skills_2':None}
        return item


# procedimiento ===============================================================
def current_urls_in_db():
    data = pn.read_json("urls_linkedin.json")
    current_urls = data["url"].tolist()
    return current_urls

def get_items_reforma(current_urls, driver,mail="raquel.sanchez@hays.com.mx",key="Rnnm345"):
    # AÑADIR ESTAS SECCIONES A LA LIMPIEZA DE SECCIONES

    #add new urls to url database
    add_new_url_list("mobile.json")

    #check which urls in list are not in detalle
    urls = obtain_url_list()
    print 'urls to record obtained'
    driver = login_linkedin()
    items = []
    views = 0
    for url in urls:
        views += 1
        item = get_profile_data(driver,url)
        items.append(item)
        if views == 650:
            start_urls = ['https://www.linkedin.com/uas/login?session_redirect=https%3A%2F%2Fwww%2Elinkedin%'
                           '2Ecom%2Fvsearch%2Fp%3Fkeywords%3DIT%252C%2Bmanager%26locationType%3DI%26rsid'
                           '%3D851944331435298366307%26orig%3DADVS%26countryCode%3Dmx%26openAdvancedForm%3Dtrue&fromSignIn=']
            driver.get(start_urls[0])
            time.sleep(10)
            driver.find_element_by_id("session_key-login").send_keys(mail)
            driver.find_element_by_id("session_password-login").send_keys(key)
            bttn = driver.find_element_by_id("btn-primary")
            bttn.click()
            time.sleep(10)
        else:
            pass
    #construct dict
    items_dicts = [dict(it) for it in items]

    try:
        df = pn.DataFrame(items_dicts)
        df['fecha_insercion'] = str(pn.datetime.today())
        print(df.head())
    except:
        pass

    detalle_old = pn.read_json("linkedin_detalle")
    data = df.append(detalle_old)
    data.reset_index(drop=True, inplace=True)
    data = data.drop_duplicates(subset="url")

    def find_item(item,text):
        if pn.isnull(text) or text == '':
            return 0
        elif isinstance(text, str) or isinstance(text, unicode):
            if re.search(item,lower(text)):
                return 1
            else:
                return 0
        else:
            return 0

    list = [" pmp "," pmi ","microstrategy","banking","tableau","qlickview","project","consultant","mobile","android",
            "ios"]
    dict = {
        " pmp ":" pmp ",
        " pmi ":" pmi ",
        "microstrategy":"microstrategy",
        "banking":"banking|banca",
        "tableau":"tableau",
        "qlickview":"qlickview",
        "project":"project|proyecto",
        "consultant":"consultant|consultor",
        "mobile":"mobile|móvil",
        "android":"android",
        "ios":" ios "
    }

    for each in list:
        data[each.strip()] = 0
        data[each.strip()] = data.apply(lambda x: find_item(dict.get(each),x["full_content"]),axis=1)


    data.to_json("linkedin_detalle")
    data = pn.read_json("linkedin_detalle")
    del data["nombre"]
    del data["descripcion"]
    del data["snippet"]
    del data["ubicacion"]
    del data["similar"]
    #get exportable data
    extra = pn.read_json("urls_linkedin.json")

    data = pn.merge(data,extra, on="url",how="left")
    data_csv = data[[u'nombre',u'descripcion',u'ubicacion',u'education_sum',u'url',u'similar',
                      u'espanol',u'frances',u'ingles', u'otro_lenguaje',
                      u'pmi',u'pmp',u'qlickview',u'tableau',u'project',u'consultant',u'banking', u'microstrategy',
                     u'mobile',u'ios',u'android']]
    data_csv.to_csv("perfiles_hays.tsv",sep="|",encoding="utf8",index=False)
    #a = data[(data["project"]==1) & (data["banking"]==1) & (data["consultant"]==1) & (data["microstrategy"]==1)]
