import sys
sys.path.append('../src/')

import loader
import numpy as np
import pandas as pd
from datetime import datetime as dt

from typing import Sequence

import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker

from arch.unitroot.unitroot import DFGLS
from statsmodels.tsa.stattools import coint, ccf, acf, pacf
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import statsmodels.api as sm

plt.rcParams['font.family'] = 'Adobe Caslon Pro'
plt.rcParams['font.size'] = 12


macro_data = loader.startupMacro()
data = macro_data.load()
data.loc[:,"COVID"] = (data.index > "2020-04-01").astype(int)

def gen_summary(dfgls_test, name:str="unnamed") -> dict:
	summ = dfgls_test.summary().tables[0].data
	summ = {i:j for i,j in summ}
	summ["Variable"] = name
	return summ

col1 = "Start-up grant for non-unemployed"
test_1 = DFGLS(data[col1], max_lags=12, method="bic")

col2 = "Start-up grant for unemployed"
test_2 = DFGLS(data[col2], max_lags=12, method="bic")

test_results = pd.DataFrame([
	gen_summary(test_1, name=col1), 
	gen_summary(test_2, name=col2)
	]).set_index("Variable")

print(test_results)