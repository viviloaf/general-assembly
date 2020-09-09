# Hard Coded City Dictionary
# This can be accessed through the object
city_dict = {
    "Atlanta": "atl.csv",
    "Austin": "atx.csv",
    "Boston": "bos.csv",
    "Chicago": "chi.csv",
    "Denver": "den.csv",
    "Los Angeles": "lax.csv",
    "New York": "nyc.csv",
    "San Francisco": "sf.csv",
    "Seattle": "sea.csv",
    "Washington, DC": "dc.csv"
    }

class ETL(object):
    def __init__(self):
        # Import libraries here.
        import numpy as np
        import pandas as pd
        import os
        import datetime as dt

        # Obtain list of files, then sort by .xlsx extension
        files = pd.Series(os.listdir('./data'))
        files = files[files.str.contains('.xlsx')]

        if os.path.isfile('./output') == True:
            pass
        else:
            files = os.listdir('./data')
            files = pd.Series(files)
            files = files[files.str.contains('.xlsx')]

    def process_data(self, file, city):
        '''
        This function processes in excel files
        Pass the file with the relative or absolute filepath
        Pass in a city that exists as a sheet name
        
        Eg:
        
        process_data('./data/jan 1.xlsx', 'Atlanta')
        '''
        # This portion copies in our PLU library and prepares it
        plu = pd.read_csv("plu-codes.csv")
        plu.set_index('plu_code', inplace=True)
        
        # This portion passes in your input strings
        # Changes index to PLU code, converts European units to American Units
        # Removes redundant columns
        # Returns a completed Dataframe that is assignable to a filename


        return_filename = file[7:-5]
        #print(return_filename)
        excel_month = return_filename.split(sep=' ')[0]
        excel_day = return_filename.split(sep=' ')[1]
        
        excel = pd.read_excel(file, sheet_name=city)
        excel.rename(columns={'prodcode': 'plu_code'}, inplace=True)
        excel.set_index('plu_code', inplace=True)
        excel['price_usd'] = excel['price_eu'] * 1.1
        excel['weight_lb'] = excel['weight_kg'] * 2.2
        excel_complete = pd.merge(excel, plu, how='left', on='plu_code')
        excel_complete.drop(['price_eu', 'weight_kg'], axis=1, inplace=True)
        excel_complete['date'] = dt.datetime(2020, 1, int(excel_day))
        return excel_complete
        
    def df_to_csv(self, input_df, input_dict, city):
        '''
        This function takes in a dataframe and

        Takes in a dict input for City to filename
        Resets any modified index and moves the index to a column
        Appends a new column for city passed as a string
        Rearranges the columns to this format:
        ['city', 'date', 'product', 'plu_code', 'quantity', 'weight_lb', 'price_usd']
        outputs each Dataframe to its own csv file
        Returns the new Dataframe as a sideproduct
        '''
        input_df = input_df.reset_index(level=None, drop=False, inplace=False, col_level=0, col_fill='')
        input_df['city'] = city
        input_df = input_df.loc[:, ['city', 'date', 'product', 'plu_code', 'quantity', 'weight_lb', 'price_usd']]
        input_df.to_csv(f'./output/{input_dict.get(city)}')
        return input_df

    def multiple_to_csv(self, input_dict=city_dict):
        '''
        Pass in a dict of cities and filenames to run functions: df_to_csv( process_data )

        city_dict is passed by default if you have no input. See below
        
        # Hard Coded City Dictionary
        city_dict = {
            "Atlanta": "atl.csv",
            "Austin": "atx.csv",
            "Boston": "bos.csv",
            "Chicago": "chi.csv",
            "Denver": "den.csv",
            "Los Angeles": "lax.csv",
            "New York": "nyc.csv",
            "San Francisco": "sf.csv",
            "Seattle": "sea.csv",
            "Washington, DC": "dc.csv"
        }

        Usage Example:

        <filename> = multiple_to_csv(input_dict)
        '''
        city_list = [i for i,j in input_dict.items()]
        
        final = []
        for j in range(len(city)):
            final.append(df_to_csv(pd.concat([process_data(f'./data/{i}', city[j]) for i in files]), city_dict, city[j]))
        return final