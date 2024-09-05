import pandas as pd
import rebrick
import streamlit as st

# Initialize the Rebrickable API with your API key
client = rebrick.Rebrick(api_key=st.secrets["apit"])

# Read color data to match to Rebrickable color IDs
color_database = pd.read_csv("Data/colors.csv")

def get_color_name(color_id):
    return color_database[color_database["id"] == color_id]["name"].values[0]

@st.cache_data
def find_sets_containing_parts(part_ids, part_colors):
    """Finds all the sets containing the provided list of parts and colors
    """
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
def find_sets_single_part(part_id, part_color):
    # Query the sets containing this part
    sets_with_part = client.get_part_color_sets(part_id, part_color)

    # Convert the results to a set of set numbers
    set_ids = {item.collection_id for item in sets_with_part}

    return set_ids

@st.cache_data
def find_part_image(part_id, part_color):
    # Get element ID
    ID = client.get_element_ids(part_id, part_color)
    
    if not ID:
        return None
    
    # If ID is a list, keep the last element, otherwise keep it as is
    ID = ID[-1] if isinstance(ID, list) else ID

    # Get element image
    img_data = client.get_element_image(ID)
    return img_data

@st.cache_data
def find_set_image(set_id):
    # Get set image
    img_data = client.get_set_image(set_id)
    return img_data

@st.cache_data
def is_part(part_id, part_color):
    # Check if part exists
    try: 
        ID = client.get_element_ids(part_id, part_color)
    except:
        return False
    
    if not ID:
        return False
    else:
        return True
    
@st.cache_data
def find_set_name(set_id):
    # Get set name
    set_name = client.get_set(set_id)
    return set_name.name