from typing import Dict, List
import numpy as np
import pandas as pd
from arch.unitroot.unitroot import DFGLS
from statsmodels.tsa.stattools import acf, pacf


class _DFGLSTest_initializer:
    def __init__(self, data, name="var") -> None:
        self.data_dict = {}
        self.results = list()
        if isinstance(data, pd.DataFrame):
            names = [
                k
                for k, v in data.dtypes.to_dict().items()
                if np.issubdtype(v, np.number)
            ]
            self.data_dict = {col: data[col].values for col in names}
        elif isinstance(data, (list, tuple)):
            for i, arr in enumerate(data):
                try:
                    if np.issubdtype(arr, np.number):
                        self.data_dict["var{i}".format(i=i)] = arr
                except TypeError:
                    print("variable at index {i} is not of type np.array".format(i=i))
                except Exception as e:
                    print(f"An error occurred: {e}")
        elif isinstance(data, np.ndarray):
            if len(data.shape) == 1:
                self.data_dict[name] = data
            else:
                if data.shape[1] > data.shape[0]:
                    data = data.T
                for col in range(data.shape[1]):
                    arr = data[:, col]
                    if np.issubdtype(arr, np.number):
                        self.data_dict["var{i}".format(i=col)] = arr
        else:
            raise TypeError("Provided data is not supported")

    def _gen_dfgls_dict(self, series: np.ndarray, name: str) -> Dict:
        dfgls = DFGLS(series, max_lags=24, method="bic", trend="ct").summary()
        dfgls = {k: v for k, v in dfgls.tables[0].data}
        dfgls["variable"] = name
        return dfgls

    def _gen_results_table(self):
        return pd.DataFrame(self.results).set_index("variable")


class DFGLSTest(_DFGLSTest_initializer):
    def __init__(self, data, name="var"):
        _DFGLSTest_initializer.__init__(self, data=data, name=name)
        self.results = [self._gen_dfgls_dict(v, k) for k, v in self.data_dict.items()]
        self.results = self._gen_results_table()

    def summary(self):
        test_desc: str = """
Trend: Constant
Critical Values: -2.66 (1%), -2.04 (5%), -1.72 (10%)
Null Hypothesis: The process contains a unit root.
Alternative Hypothesis: The process is weakly stationary.
"""
        print(self.results)
        print(test_desc)