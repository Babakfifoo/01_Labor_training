import sys
import json
from dataclasses import dataclass
import pandas as pd
import requests
from pyjstat import pyjstat

sys.path.append("../src/")


def load_json_query(fpath: str) -> dict:
    with open(fpath, encoding="utf-8") as f:
        query = json.loads(f.read())
    return(query)

STATFI_API_URL: str = "https://pxdata.stat.fi:443/PxWeb/api/v1/en/StatFin/"

@dataclass
class statfiAPIConfig:
    title: str
    url: str
    query: dict
    def load(self) -> pd.DataFrame:
        r = requests.post(STATFI_API_URL + self.url, json=self.query)
        data = pyjstat.Dataset.read(r.text).write("dataframe")
        return(data)


startupGrants = statfiAPIConfig(
    title="Startup Grant Applications",
    url="tyonv/statfin_tyonv_pxt_12u6.px",
    query=load_json_query("query/01_startup_grants.json"),
)

startupGrantsByOccupatione = statfiAPIConfig(
    title="Startup Grant Applications by Occupation",
    url="tyonv/statfin_tyonv_pxt_12u7.px",
    query=load_json_query("query/02_statup_grants_by_occupation.json"),
)

unemploymentRate = statfiAPIConfig(
    title="Unemployment Rate",
    url="tyonv/statfin_tyonv_pxt_12tf.px",
    query=load_json_query("query/03_unemployment_rate.json"),
)

