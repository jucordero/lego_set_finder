import pandas as pd
import streamlit as st
import rebrick_utils

part_database = pd.read_csv("Data/parts_clean.csv")

def get_part_name(part_id):
    return part_database[part_database["part_num"] == part_id]["name"].values[0]

@st.cache_data
def get_part_num(name):
    return part_database[part_database["name"] == name]["part_num"].values[0]

def add_part(part, color):
    # Add part to parts list
    if (part, color) not in st.session_state["parts"]:
        if rebrick_utils.is_part(part, color):
            st.session_state["parts"].append((part, color))

            # Also add part to recent list
            pl, cl = zip(*st.session_state["parts"])
            for (p, c) in zip(pl, cl):
                if (p,c) not in st.session_state["recent"]:
                    st.session_state["recent"].append((p, c))
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
    st.rerun()

def add_part_from_recent(add_recent_bool_list):
    recent_to_add = [item for i, item in enumerate(st.session_state["recent"]) if add_recent_bool_list[i]]
    if recent_to_add[0] not in st.session_state["parts"]:
        st.session_state["parts"].append(recent_to_add[0])
        st.rerun()
    else:
        st.warning("Part already added")
