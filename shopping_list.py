import streamlit as st
from datetime import datetime, date
import calendar
from isoweek import Week
from deta import Deta

#---SETTINGS---#
page_title = "Shopping List App"
page_icon = ":pouch:"
layout = "centered"

#---PAGE CONFIG---#

st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
st.title(f"{page_title} {page_icon}")

#---PERIOD VALUES---#
year = datetime.today().year
month = datetime.today().month
day = datetime.today().day
months = list(calendar.month_name[1:])
week_number = date(year, month, day).isocalendar()[1]
week = Week(year, week_number)
week_plus1 = Week(year, week_number+1)



#---DICT INIT---#
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



#---INPUT FORM---#

st.header(f"Shopping list for week from Thursday {week.thursday()} to Wednesday {week_plus1.wednesday()}")
"---"
with st.form("entry_form", clear_on_submit=True):
    st.subheader(f"Enter item for shopping list: ")
    
    for k, value in shopping_list.items():
        st.text_input(f"{shopping_list[k]['title']}:", key=k)
                
    "---"
    submitted = st.form_submit_button("Save shopping list items")     
    if submitted:
        
        period =  f"Shopping list for week from Thursday {week.thursday()} to Wednesday {week_plus1.wednesday()}"  
        
        for key, value in shopping_list.items():
            
            
            if st.session_state[key] is not '':
                items = st.session_state[key].split(",")
                for item in items:
                    item = item.strip()
                    shopping_list[key]['items'].append(item)
            st.write(len(shopping_list[key]['items']))        
            
        # categories = {categorie: st.session_state[categorie] for categorie in categories}
        
        # shopping_list = {value['items'] = st.session_state[key] for key, value in shopping_list.items()}
        # # for key, value in enumerate(categories):
        #     if categories[value]:
        #         st.write(value)
        #         items = categories[value].split(",")
        #         for item in items:
        #             item = item.strip()
        #             shopping_list[value].append(item)
            
            
            # if categories[value]:
            #     st.write(f"--{categories[value]}")
        # shopping_list.update(categories)
        

st.write("Shopping List")
st.write(shopping_list)
# for key,value in shopping_list.items():
           
#             st.write(value['items'])




#categories = ["Fruit and Veggies", 
#               "Fresh meat and fish", 
#               "Housekeeping supplies", 
#               "Potatoes, rice, pasta, etc", 
#               "Snacks", "Dairy", "Personal care", 
#               "Pets", 
#               "Beverages", 
#               "Spices and condiments", 
#               "Frozen"]