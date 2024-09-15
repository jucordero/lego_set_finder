import pandas as pd
import streamlit as st
import rebrick_utils

def add_part(part, color, name, apit):
    """
    Add part to the search list.
    """
    if (part, color, name) not in st.session_state["parts"]:
        if rebrick_utils.is_part(part, color, apit):
            st.session_state["parts"].append((part, color, name))

            # Also add part to recent list
            pl, cl, nl = zip(*st.session_state["parts"])
            for (p, c, n) in zip(pl, cl, nl):
                if (p,c,n) not in st.session_state["recent"]:
                    st.session_state["recent"].append((p, c, n))
            st.rerun()

        else:
            return "not found! Make sure the part/color combination is exists."
    else:
        return "already added to the search list!"

def reset_parts():
    st.session_state["parts"] = []
    st.rerun()
    
def remove_part(remove_part_bool_list):
    part_to_remove = [item for i,
                      item in enumerate(st.session_state["parts"]) if remove_part_bool_list[i]]
    st.session_state["parts"].remove(part_to_remove[0])
    st.rerun()

def recolor_part(change_color_bool_list, color):
    i_recolor = change_color_bool_list.index(True)
    st.session_state["parts"][i_recolor] = (st.session_state["parts"][i_recolor][0], color)
    st.rerun()

def remove_recent(remove_recent_bool_list):
    recent_to_remove = [item for i, item in enumerate(st.session_state["recent"]) if remove_recent_bool_list[i]]
    st.session_state["recent"].remove(recent_to_remove[0])

def add_part_from_recent(add_recent_bool_list):
    recent_to_add = [item for i, item in enumerate(st.session_state["recent"]) if add_recent_bool_list[i]]
    if recent_to_add[0] not in st.session_state["parts"]:
        st.session_state["parts"].append(recent_to_add[0])
    else:
        st.warning("Part already added")
