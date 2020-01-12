# Dependencies
import pandas as pd
import requests

# Normalize json file to fit a dict, then a dataframe
from pandas.io.json import json_normalize

# Import API key
from api_keys import api_key


class Drugs:
    
    # API key to OpenFDA
    api_key = api_key
    
    # Creting an empty dataframe to store results
    df_data = pd.DataFrame()

    # Constructor
    def __init__(self):
            self.data = []

    # Get Patient reaction count
    def get_patient_reaction_count(self):
        # Elements to search and url creation
        search = f"patient.reaction.reactionmeddrapt.exact"
        url = f"https://api.fda.gov/drug/event.json?api_key={api_key}&count={search}"

        # Calling API and store response as json
        r = requests.get(url)
        result = r.json()
        
        # Converting json response to a dictionary then to a Dataframe        
        return pd.DataFrame.from_dict(json_normalize(result["results"]), orient='columns')
    
    

    # Get a druga name
    def get_drug_name(self, name):
        # Elements to search and url creation
        search = f"openfda.brand_name:\"{name}\""
        url = f"https://api.fda.gov/drug/label.json?api_key={api_key}&search={search}"
        
        

        # Calling API and store response as json
        r = requests.get(url)
        result = r.json()
        
        # Converting json response to a dictionary then to a Dataframe        
        return result
#     pd.DataFrame.from_dict(json_normalize(result["results"]), orient='columns')
    
    
    
    

