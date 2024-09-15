import streamlit as st
import numpy as np

import rebrick_utils
import part_list_utils

max_recent_cols = 5

def recent_parts_menu(apit):
    if "recent" not in st.session_state:
        st.session_state.recent = []

    st.write("Recently used parts")
    reset_recent = st.button("Reset")

    if reset_recent:
        st.session_state["recent"] = []
        st.rerun()

    col3_cols = st.columns(max_recent_cols)

    add_recent_bool_list = [False] * len(st.session_state["recent"])
    remove_recent_bool_list = [False] * len(st.session_state["recent"])
    
    for i, (part, color, name) in enumerate(st.session_state["recent"]):
        with col3_cols[i%max_recent_cols]:
            img = rebrick_utils.find_part_image(part, color, apit)
            if img is not None and img != "noapi":
                st.image(img, width=40)
            add_recent_bool_list[i] = st.button("add", key=f"add_recennt_{i}")
            remove_recent_bool_list[i] = st.button("remove",
                                                   key=f"remove_recent_{i}")
            
    # Remove tuples from st.session_state["recent"] based on reset_bool_list
    if np.any(remove_recent_bool_list):
        part_list_utils.remove_recent(remove_recent_bool_list)
        st.rerun()

    # Add parts to st.session_state["parts"] based on add_bool_list
    if np.any(add_recent_bool_list):
        part_list_utils.add_part_from_recent(add_recent_bool_list)
        st.rerun()