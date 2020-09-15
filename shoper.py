import os
import pandas as pd
import git
from operator import itemgetter
from re import search


def deactivate_products(database, dc_price, replacement_price):
    """
    Deactivates products set with exact price - e.g. 107.99
    Products are kept because some of them have been withdrawn,
    yet they might come back
    
    csv_file: .csv file to work with
    dc_price: exact price that triggers deactivation of product
    column_types: column types ensuring proper encoding of file
    """
    print("\nDeactivated following products:")
    
    for row in range(database.shape[0]):
        
        if pd.isnull(database.loc[row, 'price']) == True:
            database.at[row, 'price'] = replacement_price
            database.at[row, 'active'] = 0
            print(database['name'][row],"at code", database['product_code'][row])
    

def repair_dateprices(database, months):
    """
    Repairs date prices (10.99 [meant] -> oct.99 [edited] -> 10.99)
    caused by editing the .csv file in Excel, while Shoper needs the meant ones
    
    csv_file: .csv file to work with
    months: dictionary of area-specified month names e.g. 'Jan':'1'
    column_types: column types ensuring proper encoding of file
    """

    print("Replaced following prices:")
    
    for row in range(database.shape[0]):
        
        price_value = str(database['price'][row])
        price = price_value[:3]

        if price in months.keys():
            
            new_price = price_value.replace(price, months[price])
            database.at[row, 'price'] = new_price
            print(database['price'][row], "at code", database['product_code'][row])


def linktoimage(database, folder_address, url_address):
    """
    Connects created links to exact .csv records - e.g. item codes
    If more e.g. photo names are in format "code.xxx", "code_1.xxx"
    they can be connected to additional fields like image_1, image_2 etc.
    
    csv_file: .csv file to work with
    folder_address: address of a folder containing photo folders
    column_types: column types ensuring proper encoding of file
    """

    folders = []
    sorted_pl = []
    
    for folder in os.listdir(folder_address):  # folder in list of folders
        if os.path.splitext(folder)[1] == "":  # no extension == folder
            folders.append(folder)

    for folder in folders:
        path = folder_address + folder

        for file in os.listdir(path):
            file_name = os.path.splitext(file)[0]
            image_prefix = f'{str(file_name)[:-2]}_'
            
            if search(image_prefix, file_name)!=None:
                
                if int(file_name[:-2]) in database['product_code'].values:
                    
                    sorted_pl.append([url_address + folder + "/" + file,
                                      int(file_name[:-2]), int(file_name[-1])])
    
            if int(file_name) in database['product_code'].values:
                
                sorted_pl.append([url_address + folder + "/" + file,
                                  int(file_name), 0])
    
    sorted_pl = sorted(sorted_pl, key=itemgetter(1, 2))
    product_no = 1
        
    for photolink in range(len(sorted_pl)):
        
        image_number = sorted_pl[photolink][2] + 1
        imageno_string = f'images {image_number}'
        
        if photolink!=0:
            
            if sorted_pl[photolink][1]!= sorted_pl[photolink-1][1]:
                product_no = product_no + 1
       
        database.at[product_no -1, imageno_string] = sorted_pl[photolink][0]


months_PL = {'sty': '1', 'lut': '2', 'mar': '3', 'kwi': '4',
             'maj': '5', 'cze': '6', 'lip': '7', 'sie': '8',
             'wrz': '9', 'paź': '10', 'lis': '11', 'gru': '12'}

DEFAULT_URL_ADDRESS = "https://parts.shop.pl/upload/zdjecia/"
DEFAULT_FOLDER_ADDRESS = "zdjecia/"

column_types = {'images 1': object, 'images 2': object, 'images 3': object,
                'images 4': object, 'images 5': object, 'images 6': object,
                'images 7': object, 'images 8': object, 'images 9': object,
                'price': float, 'description': object}

#csv_file = "ps_database"
#
#dataframe = pd.read_csv(csv_file + ".csv", sep=';', encoding='utf-8')
#
#repair_dateprices(dataframe, months_PL)
#deactivate_products(dataframe,"", "9999.99")
#
#for col, col_type in column_types.items():  #data type change for next function
#        dataframe[col] = dataframe[col].astype(col_type)
#        
#linktoimage(dataframe, DEFAULT_FOLDER_ADDRESS, DEFAULT_URL_ADDRESS)
#dataframe.to_csv(f'{csv_file}_updated.csv',sep=';', na_rep = '', 
#                 float_format = '%.2f', index=False, encoding='utf-8')      
my_repo = git.Repo('shoper')

