import sys
sys.path.append('../src/')

import json
import requests
import pandas as pd
import config as cfg

from pyjstat import pyjstat
from dataclasses import dataclass

@dataclass
class statfiConfig:
    query: str
    url: str
    title: str="Untitled config"
    

class statfi_loader:
    def __init__(self, config) -> None:
        
        self.config = config
        self.api_url = cfg.STATFI_API_URL + config.url

    def load_data(self) -> pd.DataFrame:
        """Loading the data from the API

        Returns:
            pd.DataFrame: a dataframe containing the requested data
        """
        r = requests.post(self.api_url, json=cfg.STARTUP_QUERY)
        data = pyjstat.Dataset.read(r.text).write("dataframe")
        
        return data

class startupMacro:
    
    def __init__(self) -> None:
        self.config = statfiConfig(
            # the query file (json file with the query for the API)
            query= "query/startup_total.json",
            url= "tyonv/statfin_tyonv_pxt_12u6.px"
        )

        self.loader = statfi_loader(self.config)

    def get_data(self) -> pd.DataFrame:
        """getting the raw dataframe from the API

        Returns:
            pd.DataFrame: the raw data as recieved from the API
        """        
        return self.loader.load_data()

    def load(self) -> pd.DataFrame:
        """loading and cleaning the data
        The data is processed and cleaned. Data types are set and the date is set as the index.

        Returns:
            pd.DataFrame: _description_
        """        
        data = self.get_data()
        data.Month = pd.to_datetime(data.Month, format="%YM%m") + pd.offsets.MonthEnd(0)
        data = data.pivot_table(
            index="Month", 
            columns="Type of employment activity", 
            values="value"
        )
        data = data.apply(pd.to_numeric, errors="coerce")
        
        return data


