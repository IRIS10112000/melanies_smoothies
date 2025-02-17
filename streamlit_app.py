# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize your Smoothie :cup_with_straw:")
st.write(
    """
    **Choose the fruits you want in your custom Smoothie!**
    """
)

name_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be: ", name_order)

cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients = st.multiselect(
    "Choose 5 ingredients: ",
     my_dataframe,
     max_selections=5
)
boton_insert= st.button('Submit Order')

if ingredients:
    ingredients_string = ' '

    for fruit_chosen in ingredients:
        ingredients_string += fruit_chosen + ' '
    
    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_order)
            values ('""" + ingredients_string + """', '""" + name_order +  """' )"""

    #st.write(my_insert_stmt)

    if boton_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")

# New Section
import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
st.text(smoothiefroot_response.json())

