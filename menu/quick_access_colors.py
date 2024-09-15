import streamlit as st
import rebrick_utils
import part_list_utils

def quick_access_color_menu(part, part_name, apit):
    with st.expander("Configure quick access colors"):
        quick_access_colors = st.multiselect("Quick access colors",
            rebrick_utils.color_database["id"],
            format_func=rebrick_utils.get_color_name)

        if quick_access_colors:
            st.session_state["quick_access_colors"] = quick_access_colors

    for c in st.session_state["quick_access_colors"]:

        col_sample, col_color_buttons = st.columns((1,5))
        
        with col_color_buttons:
            if st.button(rebrick_utils.get_color_name(c)):
                part_list_utils.add_part(part, c, part_name, apit)
        
        with col_sample:
            st.color_picker("Sample color", "#"+rebrick_utils.get_color_rgb(c),
                label_visibility="collapsed")