import sys
import os
import json
from dataclasses import dataclass
from typing import Dict, Optional, Callable, Tuple

import dataCleaners

import pandas as pd
import requests
from pyjstat import pyjstat

sys.path.append("../src/")
sys.path.append("../")

STATFI_API_URL: str = "https://pxdata.stat.fi:443/PxWeb/api/v1/en/StatFin/"

def load_json_query(fpath: str) -> dict:
    with open(fpath, encoding="utf-8") as f:
        query = json.loads(f.read())
    return(query)


def load_raw_data(APIConfig) -> pd.DataFrame:
    """This functionality allows for loading the data using the data class itself
    This method is coded to make the code readable in action.
    The resulted data is in raw format, obtained from the Statistics Finland API.
    The data cleaning and processing must be done in a separate module.

    Returns:
        pd.DataFrame: Dataframe of the raw data. 
    """
    print("Loading {title} data ...".format(title = APIConfig.title))
    path = (
        APIConfig.query # query json file
        .replace("queries","data") # changing to data dir
        .replace("json", "parquet") # Setting file type
        )
    
    if os.path.exists(path):
        print('The data file exists')
        data = pd.read_parquet(path)
        
    else:
        print('The data file does not exist')
        queryDict = load_json_query(APIConfig.query)
        r = requests.post(STATFI_API_URL + APIConfig.url, json=queryDict)
        data = pd.DataFrame(pyjstat.Dataset.read(r.text).write("dataframe"))
        data.to_parquet(path) 
        
    print("{title} Data loaded.\n\n".format(title = APIConfig.title))
    return data
    

@dataclass
class statfiAPIConfig():
    """This data class generates all components necessary for loading data from Statistics Finland Open Database 
    """    
    title: str # Name of the data. It is based on the data itself and the query
    url: str # URL of the API for getting the data. This is not the Data source page!
    query: str # A Dictionary made from JSON query tailored for the project.
    raw_data: Optional[pd.DataFrame] = None
    labels: Optional[Dict[str,str]] = None
    cleaned_data: Optional[pd.DataFrame] = None
    data_processing_function: Optional[Callable[[pd.DataFrame], Tuple[Dict[str,str], pd.DataFrame]]] = None # cleaning function added here
    
    def load(self) -> None:
        self.raw_data = load_raw_data(self)
        if self.data_processing_function is not None:
            self.labels, self.cleaned_data = self.data_processing_function(self.raw_data)

# TODO: impolement storing method that checks whether the data exists. 
# TODO: Specify the file format for storing the loaded data.

startupGrants = statfiAPIConfig(
    title="Startup Grant Applications",
    url="tyonv/statfin_tyonv_pxt_12u6.px",
    query="../queries/01_startup_grants.json",
    data_processing_function=dataCleaners.cleanSturtupGrants
)

startupGrantsByOccupatione = statfiAPIConfig(
    title="Startup Grant Applications by Occupation",
    url="tyonv/statfin_tyonv_pxt_12u7.px",
    query="../queries/02_statup_grants_by_occupation.json",
    data_processing_function=None # FIX
)

employmentRate = statfiAPIConfig(
    title="Employment Rate",
    url="tyonv/statfin_tyonv_pxt_12tf.px",
    query="../queries/03_unemployment_rate.json",
    data_processing_function=dataCleaners.cleanEmploymentRate
)

# TODO: This is data cleaning Method for specific class:

