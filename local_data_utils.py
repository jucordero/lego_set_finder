import pandas as pd
import streamlit as st

set_inventory_id = pd.read_csv("Data/inventories.csv")
inventory_parts = pd.read_csv("Data/inventory_parts.csv")


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

if __name__ == "__main__":
    print(find_sets_single_part("3001", 1))
    print(find_sets_containing_parts(["3001", "3002"], [1, 1]))
