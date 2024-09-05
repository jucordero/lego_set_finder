import streamlit as st
import numpy as np
import pandas as pd

import rebrick_utils
import part_list_utils
import local_data_utils

# Layout config
st.set_page_config(layout='wide')

max_parts_cols = 7
max_recent_cols = 5

# define session state variables
if 'parts' not in st.session_state:
    st.session_state.parts =  []

if "recent" not in st.session_state:
    st.session_state.recent = []

remove_part_bool_list = [False] * len(st.session_state["parts"])
change_color_bool_list = [False] * len(st.session_state["parts"])
add_recent_bool_list = [False] * len(st.session_state["recent"])
remove_recent_bool_list = [False] * len(st.session_state["recent"])

# Helpers
rb_set_url = "https://www.rebrickable.com/sets/"

# Main layout
col_inputs, col_colors, col_recent = st.columns((2,0.5,1))

with col_inputs:

    with st.container():
        col1, col2 = st.columns((1,1))

        with col1:
            # part = st.text_input("Select part number")
            part_name = st.selectbox("Select part",
                                part_list_utils.part_database["name"])
            part = part_list_utils.get_part_num(part_name)
                                
            add_part = st.button("Add part")

        with col2:
            color = st.selectbox("Select color",
                                rebrick_utils.color_database["id"],
                                format_func=rebrick_utils.get_color_name) 
            reset_part = st.button("Reset items")

    st.divider()

    if add_part:
        # If results returns a value, this means the part was not found
        # Otherwise, the function reruns the app and never gets to the warning.
        result = part_list_utils.add_part(part, color)
        st.warning("Part " + result)

    if reset_part:
        part_list_utils.reset_parts()

    # Add parts images
    item_cols = st.columns(max_parts_cols)
    if st.session_state["parts"]:
        for i, (p, c) in enumerate(st.session_state["parts"]):
            with item_cols[i%max_parts_cols]:
                img = rebrick_utils.find_part_image(p, c)
                if img is None:
                    st.write("Image not found")
                else:
                    st.image(img, width=100)

                remove_part_bool_list[i] = st.button("remove",
                                                     key=f"remove_part{i}")
                change_color_bool_list[i] = st.button("change color",
                                                      key=f"change_color{i}")
    else:
        st.write("Add parts to see them here")

    # If any button has been pressed
    if np.any(remove_part_bool_list):
        part_list_utils.remove_part(remove_part_bool_list)

    if np.any(change_color_bool_list):
        part_list_utils.recolor_part(change_color_bool_list, color)

    st.divider()

    # Find sets
    sets = None
    if st.button("Find sets"):
        if st.session_state["parts"]:
            pl, cl = zip(*st.session_state["parts"])
            # sets = rebrick_utils.find_sets_containing_parts(pl, cl)
            sets = local_data_utils.find_sets_containing_parts(pl, cl)
        else:
            st.warning("No pieces to search!")

    if sets is None:
        st.write("Add parts and colors to find sets")
        
    else:
        for set in sets:
            st.markdown(f"[Set {set}, {rebrick_utils.find_set_name(set)}]({rb_set_url + set})")

quick_access_colors = {"Black":0, "White":15, "DBG":72, "LBG":71, "Tan":19,
                       "Dark Tan":28}

with col_colors:
    for c in quick_access_colors.keys():
        if st.button(c):
            result = part_list_utils.add_part(part, quick_access_colors[c])
            st.warning("Part " + result)

# Recently used pieces for easier access. 
with col_recent:
    st.write("Recently used pieces")
    reset_recent = st.button("Reset")

    if reset_recent:
        st.session_state["recent"] = []
        st.rerun()

    col3_cols = st.columns(max_recent_cols)

    for i, (part, color) in enumerate(st.session_state["recent"]):
        with col3_cols[i%max_recent_cols]:
            img = rebrick_utils.find_part_image(part, color)
            if img is not None:
                st.image(img, width=40)
            add_recent_bool_list[i] = st.button("add", key=f"add_recennt_{i}")
            remove_recent_bool_list[i] = st.button("remove",
                                                   key=f"remove_recent_{i}")

# Remove tuples from st.session_state["recent"] based on reset_bool_list
if np.any(remove_recent_bool_list):
    part_list_utils.remove_recent(remove_recent_bool_list)

# Add parts to st.session_state["parts"] based on add_bool_list
if np.any(add_recent_bool_list):
    part_list_utils.add_part_from_recent(add_recent_bool_list)