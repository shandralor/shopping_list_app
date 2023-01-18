from deta import Deta
import json
from pprint import pprint
import os
import streamlit as st

DETA_KEY = st.secrets.DETA_KEY
deta = Deta(DETA_KEY)

sl = deta.Base("sl")
recipes = deta.Base("recipes")

#---SHOPPING LIST FUNCTIONS---#
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

#---RECIPE FUNCTIONS

def get_recipes():
    return recipes.fetch().items, len(recipes.fetch().items)

def enter_recipe(name, ingredients, instructions, active=False):
    return recipes.put({"key" : name,"ingredients" : ingredients, "instructions" :instructions, "active" : active})

def get_recipe_status(col_nr = "a"):
    needed_recipe_list = []
    if col_nr =="a":
        for recipe in get_recipes()[0]:
            if recipe["active"] == True:
                needed_recipe_list.append(recipe)
    elif col_nr =="b":
        for recipe in get_recipes()[0]:
            if recipe["active"] == False:
                needed_recipe_list.append(recipe)
    return needed_recipe_list

def update_recipe_status(key):
    to_change= recipes.get(key)
    if to_change["active"] == False:
        changed = {"active" : True}
        recipes.update(changed, key)
    else:
        changed = {"active" : False}
        recipes.update(changed, key)
       
    
def add_ingredients_to_shopping_list(key, weeknumber):
    ingredients_to_add= recipes.get(key)
    for ingredient in ingredients_to_add["ingredients"]:
        shopping_list_update_line = {
            "shopping_list.snacks.items": sl.util.append(ingredient.strip("-"))
            }
    
        sl.update(shopping_list_update_line, weeknumber)
        
        
