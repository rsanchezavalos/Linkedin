__author__ = 'rsanchez'

import pandas as pn
import re
def clean_state(x):
    """this function has to clean state info"""
    pass
def trytofind(element,x):
    if re.search(element,x).group(0):
        return 1
    else:
        return 0


def skill_items_generator(element,on,db):
    db[element] = trytofind(element,db[on])
    pass



#scrape new data
data = pn.read_json("Hays/urls_linkedin.json")

#Comparar con base master de ids y quedarse con los nuevos.
new = set(data["url"])

#detalle query only for new ones:



#extra - data generation
data["state"] = data["ubicacion"].apply(lambda x: clean_state(x))
#list of info queries:


skill_items_generator("Proyecto","snippet",data.iloc[782])
#782