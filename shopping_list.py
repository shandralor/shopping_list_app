import streamlit as st
from streamlit_option_menu import option_menu
from datetime import datetime, date
import calendar
from isoweek import Week
import db as db
from pprint import pprint
import uuid



#---SETTINGS---#
page_title = "Weekly dinner and shopping app"
page_icon = ":pouch:"
layout = "centered"


#---PAGE CONFIG---#
st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
st.title(f"{page_title} {page_icon}")

#---STREAMLIT CONFIG HIDE---#
hide_st_style = """<style>
                #MainMenu {visibility : hidden;}
                footer {visibility : hidden;}
                header {visibility : hidden;}
                </style>
                """
st.markdown(hide_st_style, unsafe_allow_html=True)

#---PERIOD VALUES---#
year = datetime.today().year
month = datetime.today().month
day = datetime.today().day+4
months = list(calendar.month_name[1:])
week_number = date(year, month, day).isocalendar()[1]
week = Week(year, week_number)
week_plus1 = Week(year, week_number+1)


#---DICT AND LIST INIT---#
shopping_list = {
    "fruit_and_veg" : {"title" : "Fruit and Veggies", "items" : []},
    "meat_and_fish" : {"title" :"Fresh meat and fish", "items" : []},
    "housekeeping" : {"title" :"Housekeeping supplies", "items" : []},
    "carbs" : {"title" : "Potatoes, rice, pasta, etc", "items" : []},
    "snacks" : {"title" : "Snacks", "items" : []},
    "dairy" : {"title" : "Dairy", "items" : []},
    "personal_care" : {"title" : "Personal care", "items" : []},
    "pets" : {"title" : "Pets", "items" : []},
    "beverages" : {"title" : "Beverages", "items" : []},
    "spices_and_cond" : {"title" : "Spices and condiments", "items" : []},
    "frozen" : {"title" : "Frozen", "items" : []}
    }

key_dict = {
    'fruit_and_veg': [], 
    'meat_and_fish': [], 
    'housekeeping': [], 
    'carbs': [], 
    'snacks': [], 
    'dairy': [], 
    'personal_care': [], 
    'pets': [], 
    'beverages': [], 
    'spices_and_cond': [], 
    'frozen': []
    }

ingredients_dict = {
    }

instructions_dict = {
    }


#---FUNCTIONS---#


#---NAV BARS---#
nav_menu = option_menu(
    menu_title = None,
    options = ["Current Week", "Weekly recipes"],
    icons = ["list-task", "cup-straw" ],
    orientation = "horizontal"
) 

#---INPUT FORM---#
if nav_menu == "Current Week":
    
    st.header(f"Thursday {week.thursday()} to Wednesday {week_plus1.wednesday()}")
    col1, col2 = st.columns([4,4], gap = "medium")

    with col1:
        st.caption(f"Please enter items, separated by commas")
        with st.form("entry_form", clear_on_submit=True):
                        
            for k, value in shopping_list.items():
                st.text_input(f"{shopping_list[k]['title']}:", key=k)
            "---"
            
            submitted = st.form_submit_button("Save shopping list items", type = "primary")     
            if submitted:
                if db.get_shopping_list(week_number):
                    
                    for key in key_dict:
                        update_dict = {}
                        if st.session_state[key] != '':
                                items = st.session_state[key].split(",")
                                for item in items:
                                    item = item.strip()
                                update_dict[key] = items                  
                                db.update_shopping_list(str(week_number), update_dict)
                else:     
                    period =  f"Shopping list for week from Thursday {week.thursday()} to Wednesday {week_plus1.wednesday()}"  
                    for key, value in shopping_list.items():                
                        
                        if st.session_state[key] != '':
                            items = st.session_state[key].split(",")
                            for item in items:
                                item = item.strip()
                                shopping_list[key]['items'].append(item)                 
                        db.enter_shopping_list_items(week_number, period, shopping_list)      

    with col2:
        
        current_shopping_list = db.get_shopping_list(week_number)
        
        if current_shopping_list:
            st.caption("Click an item to remove it from this weeks list")
            
            for k, value in current_shopping_list["shopping_list"].items():
                #st.subheader(value["title"])
                for item in value["items"]:
                    st.button(label = item, key =f"{item}{str(uuid.uuid4())[:8]}", on_click=db.remove_item_shopping_list, args= (str(week_number), k, item))
                
        else:
            st.subheader(f"You have not created a shopping list yet for week from Thursday {week.thursday()} to Wednesday {week_plus1.wednesday()}")
            
if nav_menu == "Weekly recipes":
    col1, col2, col3 = st.columns([4,4,2], gap = "medium")
    
    
    with col1:
        st.subheader("This week's recipes:")   
        
        if len(db.get_recipe_status()) < 1:
            st.caption("This page will hold a clickable collection of recipes. \
                When you select one the idea is to both have it appear in a list on the first page and automatically add the ingredients to the shopping list.")
        else:
            st.caption("Click on a recipe to see the instructions or add the ingredients to the shopping list")
            for recipe in db.get_recipe_status():
                with st.expander(recipe["key"]):
                    "---"
                    for ingredient in recipe["ingredients"]:
                        st.write(ingredient)
                    '---'
                    for instruction in recipe["instructions"]:
                        st.write(instruction)
                    '---'
                    st.button(label = "Remove recipe from current week",key = f'{recipe["key"]}t', on_click=db.update_recipe_status, args=(recipe["key"],))
                    st.button(label = "Add ingredients to shopping list", key = f'{recipe["key"]}a', on_click=db.add_ingredients_to_shopping_list , args=(recipe["key"], str(week_number)),type = "primary")
        
        
    with col2:
        st.subheader("Enter new recipe")
        with st.form("entry_form", clear_on_submit=True):
                        
            st.text_input("Recipe Name:", key="name")
            "---"
            st.caption("Please enter ingredient amounts, separated by commas")
            st.text_area("Ingredients: ", key = "ingredients")
            "---"
            st.caption("Please enter instructions, separated by commas")            
            st.text_area("Instructions: ", key = "instructions")
            
            submitted = st.form_submit_button("Save recipe", type = "primary")
            
            if submitted:
                
                
                recipe_name = st.session_state["name"].title()
                #---
                recipe_ingredients = st.session_state["ingredients"].split(",")
                recipe_ingredients = [f"- {i.strip()}" for i in recipe_ingredients]
                #---
                recipe_instructions = st.session_state["instructions"].split(",")
                for counter, instruction in enumerate(recipe_instructions, 1):
                    print(f"{counter}. {instruction.strip().capitalize()}")
                    recipe_instructions[counter-1] = f"{counter}. {instruction.strip().capitalize()}"
                #---
                db.enter_recipe(recipe_name, recipe_ingredients, recipe_instructions)
                
            
           
    with col3:
        st.subheader("Recipe List: " )
        st.caption("Click a recipe to add it to this weeks list")
        for recipe in db.get_recipe_status("b"):
            st.button(label = recipe["key"],key = f'{recipe["key"]}f', on_click=db.update_recipe_status, args=(recipe["key"],))
                
                
    






