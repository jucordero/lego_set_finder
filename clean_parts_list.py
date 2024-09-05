"""Module for cleaning parts list.

The parts database contains a lot of parts not really useful for set finding.
It is also hard to navigate with all the printed and stickered parts.

In this script we clean the list down to a subset of parts that are useful for
set identification.

Remove prints and patterned parts
- Remove all parts with the string "Print" or "print" in the name
- Remove all parts with "pr" in the part_num field
- Remove all parts with "pat" in the part_num field

Remove sticker sheets
- Remove all parts with "Sticker" or "sticker" in the part_num field

Remove fabrics, capes, and other non-plastic and non-traditional parts
- Remove all parts with part_material value different from "Plastic"
- Remove all parts with part_num starting with a letter.

Remove non-system parts
- Remove all parts with "Duplo" in the name field
- Remove all parts with "Modulex" in the name field

"""

import pandas as pd

parts_db = pd.read_csv("Data/parts.csv")

parts_clean = parts_db[~parts_db["name"].str.contains("print")]
parts_clean = parts_db[~parts_db["name"].str.contains("Print")]
parts_clean = parts_clean[~parts_clean["part_num"].str.contains("pr")]
parts_clean = parts_clean[~parts_clean["part_num"].str.contains("pat")]

parts_clean = parts_clean[~parts_clean["name"].str.contains("Sticker")]
parts_clean = parts_clean[~parts_clean["name"].str.contains("sticker")]

parts_clean = parts_clean[parts_clean["part_material"] == "Plastic"]
parts_clean = parts_clean[parts_clean["part_num"].str.match(r'^\d')]

parts_clean = parts_clean[~parts_clean["name"].str.contains("Duplo")]

parts_clean = parts_clean[~parts_clean["name"].str.contains("Modulex")]

parts_clean.to_csv("Data/parts_clean.csv", index=False)

# This currently reduces the database size from ~50,000 items to around 8,000.


