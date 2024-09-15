import streamlit as st
import numpy as np
import pandas as pd

import part_list_utils
import rebrick_utils

part_database = pd.read_csv("Data/parts_clean.csv")

def add_parts_menu(apit):

    col1, col2 = st.columns((1,1))

    with col1:
        # part = st.text_input("Select part number")
        part_name = st.selectbox("Select part",
            part_database["name"],
            help="""Type to search for a part name. A few tips that can help you get to your piece quicker:  
            - Start by the general category of your piece (e.g. 'Plate', 'Brick', 'Slope)  
            - Most of the time a secondary characteristic follows (e.g. 'Curved', 'Round', 'Inverted')  
            - Size or dimensions (e.g. '3x2', '3', '30ª') Be sure to check the inverted dimensions  (e.g. '4x2' instead of '2x4)  
            - In some cases a secondary characteristic can be after the dimension (e.g. 'Bracket 1 x 2 - 1 x 2 Inverted')  
            - Newer tiles have a 'with groove' in their name (e.g. 'Tile 1 x 2 with groove')""")
        
        color = st.selectbox("Select color",
            rebrick_utils.color_database["id"],
            format_func=rebrick_utils.get_color_name,
            help="""Type to search for a color. Or use the
            quick access color buttons to the right""") 
        
        part = rebrick_utils.get_part_num(part_name)

    with col2:
        st.write("")
        st.write("")
        add_part = st.button("Add part")
        st.write("")
        st.write("")
        reset_part = st.button("Reset items")

    st.divider()

    if add_part:
        # If 'result' returns a value, this means the part was not found.
        # Otherwise, the function reruns the app and never gets to the warning.
        result = part_list_utils.add_part(part, color, part_name, apit)
        # st.warning("Part " + result)

    if reset_part:
        part_list_utils.reset_parts()

    return part, color, part_name

def selected_parts_menu(color, apit):

    remove_part_bool_list = [False] * len(st.session_state["parts"])
    change_color_bool_list = [False] * len(st.session_state["parts"])

    if st.session_state["parts"]:
        for i, (p, c, n) in enumerate(st.session_state["parts"]):
            sel_part_cols = st.columns((1,1,1,5))
            with sel_part_cols[0]:
                img = rebrick_utils.find_part_image(p, c, apit)
                if img == "noapi":
                    st.error("API key not specified. Please enter your API key in top text field.")
                elif img is None:
                    st.write("Image not found")
                else:
                    st.image(img, width=50)

            with sel_part_cols[1]:
                remove_part_bool_list[i] = st.button("remove", key=f"remove_part{i}")
            with sel_part_cols[2]:
                change_color_bool_list[i] = st.button("change color", key=f"change_color{i}")
            with sel_part_cols[3]:
                st.write(n)
    else:
        st.write("Add parts to see them here")

    # If any button has been pressed
    if np.any(remove_part_bool_list):
        part_list_utils.remove_part(remove_part_bool_list)

    if np.any(change_color_bool_list):
        part_list_utils.recolor_part(change_color_bool_list, color)
    
    st.divider()
