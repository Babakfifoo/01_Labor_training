import sys
from typing import Dict
sys.path.append("../src/")
import pandas as pd


def gen_end_of_month_dates(series: pd.Series, format="%YM%m") -> pd.Series:
    """Converting string Monthly data notation to actual end of the month date

    Args:
        series (pd.Series): pandas series with Monthly string notation
        format (str, optional): Defaults to "%YM%m".

    Returns:
        pd.Series: series of dates.
    """
    result = pd.to_datetime(series, format="%YM%m", errors="raise").apply(
        lambda x: (x + pd.offsets.MonthEnd(0))
    )
    return result


def cleanSturtupGrants(data: pd.DataFrame) -> tuple[Dict[str,str], pd.DataFrame]:
    """Cleaning start-up grants raw data

    Args:
        data (pd.DataFrame): raw data obtained from StatFi API

    Returns:
        tuple[dict, pd.DataFrame]: labels and the cleaned data is returned
    """
    # THE DATA LABELS ---------------------------------------------------------
    columns_labels = dict(
        grantEmp="Start-up grant for non-unemployed",
        grantUnemp="Start-up grant for unemployed",
        grantLms="Start-up grant with lms",
    )
    # -------------------------------------------------------------------------

    # Converting the month string to dates.
    data["Month"] = gen_end_of_month_dates(data["Month"])

    data = data.pivot_table(
        index="Month", columns="Type of employment activity", values="value"
    )

    data = data.rename(columns={v: k for k, v in columns_labels.items()})
    return (columns_labels, data)


def cleanEmploymentRate(data: pd.DataFrame) -> tuple[Dict[str,str], pd.DataFrame]:
    """Cleaning employment rate raw data

    Args:
        data (pd.DataFrame): raw data obtained from StatFi API

    Returns:
        tuple[dict, pd.DataFrame]: labels and the cleaned data is returned
    """
    # THE DATA LABELS ---------------------------------------------------------
    columns_labels = dict(
        unempRate = 'Proportion of unemployed jobseekers as a percentage of total workforce (%)',
        unempCount ='Unemployed jobseekers on calculation date (number)',
        workforce = 'Workforce in Statistic Finlands RES (number)'
    )
    
    data["Month"] = gen_end_of_month_dates(data["Month"])
    data = data.pivot_table(
        index="Month", columns="Information", values="value"
    )
    
    data = data.rename(columns={v: k for k, v in columns_labels.items()})
    return (columns_labels, data)