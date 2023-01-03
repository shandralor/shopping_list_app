import streamlit as st

#---SETTINGS---#

categories = ["Fruit and Veggies", "Fresh meat and fish", "Housekeeping supplies", "Potatoes, rice, pasta, etc", "Snacks", "Dairy", "Personal care", "Pets", "Beverages", "Spices and condiments", "Frozen"]
page_title = "Shopping List App"
page_icon = ":pouch:"
layout = "centered"


#---PAGE CONFIG---#

st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
st.title(f"{page_title} {page_icon}")
