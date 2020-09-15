# shoper
simple app for shoper-used .csv files

included functions:

[repair_dateprices]
repairing date prices (e.g. 1.99 -> Jan.99 (changed by Excel editing) -> 1.99 (reversing this process)), based on whether the first 3 signs of string match the keys in dict months

[deactivate_products]
deactivating products, based on its price (checks if the cell is null or matches the given dc_price) and changing it to replacement_price, being the indicator for later use

[linktoimage]
creates links based on URL_ADDRESS, adds folders and file names from FOLDER_ADDRESS, merging them into format URL_ADDRESS/FOLDER_ADDRESS/folder/filename.extension
later, it connects the created links to "images 1-9" columns for the given products based on its name, e.g. product_code == 1, it finds files called 1.extension or 1_x.extension
x+1 being used to assign the file to "images x" column

to be added:
- functional UI,
- errors (e.g. x in linktoimage exceeding 8),
- logging.
