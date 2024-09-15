import streamlit as st

import rebrick_utils

from menu.quick_access_colors import quick_access_color_menu
from menu.recent_parts import recent_parts_menu
from menu.add_parts import add_parts_menu, selected_parts_menu

# Layout config
st.set_page_config(layout='wide')

max_parts_cols = 7

# define session state variables
if 'parts' not in st.session_state:
    st.session_state.parts =  []

if "quick_access_colors" not in st.session_state:
    st.session_state.quick_access_colors = []    

# Helpers
rb_set_url = "https://www.rebrickable.com/sets/"

# Main layout
col_inputs, col_colors, col_recent = st.columns((2,0.5,1))

with col_inputs:
    apit = st.text_input("Rebrickable API token",
                          type="password",
                          help="""Get your token from your user settings page on Rebrickable.  
                          This is needed to access the Rebrickable API.""")
    
    st.session_state.apit = apit

    part, color, part_name = add_parts_menu(apit)

    selected_parts_menu(color, apit)

    # Find sets
    sets = None
    if st.button("Find sets"):
        if st.session_state["parts"]:
            pl, cl, nl = zip(*st.session_state["parts"])
            sets = rebrick_utils.find_sets_containing_parts(pl, cl)
        else:
            st.warning("No pieces to search!")

    if sets is None:
        st.write("Add parts and colors to find sets")
        
    else:
        for set in sets:
            st.markdown(f"[Set {set}, {rebrick_utils.find_set_name(set, apit)}]({rb_set_url + set})")

# Column to select quick access colors
with col_colors:
    quick_access_color_menu(part, part_name, apit)
            
# Recently used pieces for easier access. 
with col_recent:
    recent_parts_menu(apit)
