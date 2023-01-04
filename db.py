from deta import Deta
import json
from pprint import pprint
import os
from dotenv import load_dotenv

load_dotenv(".env")

DETA_KEY = os.getenv("DETA_KEY")

deta = Deta(DETA_KEY)

sl = deta.Base("sl")

def enter_shopping_list_items(weeknumber, title, shopping_list):
    return sl.put({"key" : str(weeknumber),"title":title, "shopping_list" :shopping_list})

def get_shopping_list(period):
    return sl.get(str(period))

weeknumber = 1
title = "Shopping list for week from Thursday 2023-01-05 to Wednesday 2023-01-11"
shopping_list = {
    "dairy" : ["milk"],
    "frozen" : ["pizza"],
    "pets" : ["cat food", "dog food"],
    "beverages" : []
}
# shopping_list = {"Fruit and Veggies":[],
# "Fresh meat and fish":[],
# "Housekeeping supplies":[],
# "Potatoes, rice, pasta, etc":["aardappelen", "rijst"],
# "Snacks":[],
# "Dairy":[],
# "Personal care":["toiletpapier", "tandpasta"],
# "Pets":[],
# "Beverages":[],
# "Spices and condiments":[],
# "Frozen":["pizza"]}

shopping_list_update = {

"shopping_list.beverages": sl.util.append("milk")
}



#sl.update(shopping_list_update, "1")
#enter_shopping_list_items(weeknumber, title, shopping_list)

pprint(get_shopping_list(weeknumber))