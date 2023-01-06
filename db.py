from deta import Deta
import json
from pprint import pprint
import os

import streamlit as st


DETA_KEY = st.secrets.DETA_KEY

deta = Deta(DETA_KEY)

sl = deta.Base("sl")

def enter_shopping_list_items(weeknumber, title, shopping_list):
    return sl.put({"key" : str(weeknumber),"title":title, "shopping_list" :shopping_list})

def get_shopping_list(period):
    return sl.get(str(period))



def update_shopping_list(weeknumber, update_dict):
    for key, value in update_dict.items():
        print(f"{key} {value} ")
        shopping_list_update_line = {
            f"shopping_list.{key}.items": sl.util.append(value)
            }
    
        sl.update(shopping_list_update_line, weeknumber)
    
def remove_item_shopping_list(weeknumber, key, item_to_remove):
        shopping_list_to_change = get_shopping_list(weeknumber)["shopping_list"][key]['items']
        shopping_list_to_change.remove(item_to_remove)
        print(shopping_list_to_change)
        
        shopping_list_update_line = {
            f"shopping_list.{key}.items": shopping_list_to_change
            }
    
        sl.update(shopping_list_update_line, weeknumber)


# remove_item_shopping_list(1, "beverages", "milk")