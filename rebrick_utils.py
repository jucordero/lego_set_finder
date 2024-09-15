import pandas as pd
import rebrick
import streamlit as st
from urllib.error import HTTPError

# Read part data to match to Rebrickable color IDs
color_database = pd.read_csv("Data/colors.csv")
part_database = pd.read_csv("Data/parts_clean.csv")
set_inventory_id = pd.read_csv("Data/inventories.csv")
inventory_parts = pd.read_csv("Data/inventory_parts.csv")

def get_part_name(part_id):
    return part_database[part_database["part_num"] == part_id]["name"].values[0]

def part_name_plus_id(part_id):
    return get_part_name(part_id) + " - " + part_id

@st.cache_data
def get_part_num(name):
    return part_database[part_database["name"] == name]["part_num"].values[0]

def get_color_name(color_id):
    return color_database[color_database["id"] == color_id]["name"].values[0]

def get_color_rgb(color_id):
    return color_database[color_database["id"] == color_id]["rgb"].values[0]

@st.cache_data
def find_sets_single_part(part_id, part_color):
    "Finds all the sets containing the provided part and color combination"

    inv_mask = (inventory_parts["part_num"] == part_id) \
         & (inventory_parts["color_id"] == part_color)

    inv = inventory_parts[inv_mask]

    sets_with_part = set_inventory_id[set_inventory_id["id"].isin(inv["inventory_id"])]

    return set(sets_with_part["set_num"].values)

@st.cache_data
def find_sets_containing_parts(part_ids, part_colors):
    """Finds all the sets containing the provided list of parts and colors
    combinations."""
    sets_containing_all_parts = None
    
    # Iterate through the provided part IDs
    for part_id, part_color in zip(part_ids, part_colors):
        # Query the sets containing this part
        set_ids = find_sets_single_part(part_id, part_color)
        
        # Intersect the sets to keep only those that contain all parts
        if sets_containing_all_parts is None:
            sets_containing_all_parts = set_ids
        else:
            sets_containing_all_parts.intersection_update(set_ids)

    return sets_containing_all_parts

@st.cache_data
def find_part_image(part_id, part_color, apit):

    # Initialize the Rebrickable API with your API key
    client = rebrick.Rebrick(api_key=apit)

    # Get element ID
    try:
        ID = client.get_element_ids(part_id, part_color)
    except HTTPError:
        return "noapi"
    if not ID:
        return None
     
    # If ID is a list, keep the last element, otherwise keep it as is
    ID = ID[-1] if isinstance(ID, list) else ID

    # Get element image
    img_data = client.get_element_image(ID)
    return img_data

@st.cache_data
def is_part(part_id, part_color, apit):

    # Initialize the Rebrickable API with your API key
    client = rebrick.Rebrick(api_key=apit)

    # Check if part exists
    try:
        ID = client.get_element_ids(part_id, part_color)
    except ValueError:
        st.error("API key not specified. Please enter your API key in top text field.")
        return False
    except HTTPError:
        st.error("Wrong API provided. Please check your API key.")
        return False
    
    if not ID:
        return False
    else:
        return True
    
@st.cache_data
def find_set_name(set_id, apit):
    """Get set name"""

    # Initialize the Rebrickable API with your API key
    client = rebrick.Rebrick(api_key=apit)

    set_name = client.get_set(set_id)
    return set_name.name